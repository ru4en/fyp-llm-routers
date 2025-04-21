"""
title: Tool Router
author: Ruben Lopes (@ru4en)
description: |
    This is a simple tool router that uses a zero-shot classification model to route queries to the appropriate tool.
    It uses the Hugging Face Transformers library for the zero-shot classification model.
    The router can be used to route queries to different tools based on their descriptions.
    The router can be used in a pipeline with other components.
requirements: pydantic, requests, git+https://github.com/ru4en/llm_routers.git
version: 1.0.0
"""

from llm_routers import ToolRouter
import sys

from typing import Callable, Any, List, Dict, Optional, Tuple
from pydantic import BaseModel, Field
from open_webui.models.tools import Tools
import inspect
import asyncio


class EventEmitter:
    """
    Helper wrapper for OpenWebUI event emissions.
    """

    def __init__(
        self,
        event_emitter: Callable[[dict], Any] = None,
        debug: bool = False,
    ):
        self.event_emitter = event_emitter
        self._debug = debug
        self._status_prefix = None
        self._emitted_status = False

    def set_status_prefix(self, status_prefix):
        self._status_prefix = status_prefix

    async def _emit(self, typ, data, twice):
        if self._debug:
            print(f"Emitting {typ} event: {data}", file=sys.stderr)
        if not self.event_emitter:
            return None
        result = None
        for i in range(2 if twice else 1):
            maybe_future = self.event_emitter(
                {
                    "type": typ,
                    "data": data,
                }
            )
            if asyncio.isfuture(maybe_future) or inspect.isawaitable(maybe_future):
                result = await maybe_future
        return result

    async def status(
        self, description="Unknown state", status="in_progress", done=False
    ):
        self._emitted_status = True
        if self._status_prefix is not None:
            description = f"{self._status_prefix}{description}"
        await self._emit(
            "status",
            {
                "status": status,
                "description": description,
                "done": done,
            },
            twice=not done and len(description) <= 1024,
        )

    async def fail(self, description="Unknown error"):
        await self.status(description=description, status="error", done=True)

    async def clear_status(self):
        if not self._emitted_status:
            return
        self._emitted_status = False
        await self._emit(
            "status",
            {
                "status": "complete",
                "description": "",
                "done": True,
            },
            twice=True,
        )

    async def message(self, content):
        await self._emit(
            "message",
            {
                "content": content,
            },
            twice=False,
        )

    async def citation(self, document, metadata, source):
        await self._emit(
            "citation",
            {
                "document": document,
                "metadata": metadata,
                "source": source,
            },
            twice=False,
        )

    async def code_execution(self, code_execution_tracker):
        await self._emit(
            "citation", code_execution_tracker._citation_data(), twice=True
        )


featured_tools: Dict[str, str] = {
    "web_search": "search the web for information",
    "code_interpreter": "interpret or execute python code",
    # "image_generation": "generate images if applicable",
}


class Filter:
    emitter: EventEmitter = None

    class Valves(BaseModel):
        model: str = Field(
            "facebook/bart-large-mnli",
            description="The model to use for the zero-shot classification task.",
        )
        n: int = Field(
            3,
            description="The number of tools to return.",
        )
        threshold: float = Field(
            0.8,
            description="The threshold for tool selection.",
        )
        # New parameter to control minimum probability for tool selection
        min_probability: float = Field(
            0.7,
            description="The minimum probability required to return any tool. If the highest probability is below this, no tool will be returned.",
        )

    def __init__(self):
        self.valves = self.Valves()
        self.tools = featured_tools
        self.tool_router: ToolRouter = None

    async def inlet(
        self, body: dict, __event_emitter__: Callable[[dict], Any] = None
    ) -> dict:

        self.emitter = EventEmitter(__event_emitter__)
        await self.emitter.status("Selecting tool...", status="in_progress", done=False)
        self.tools = {
            tool.id: tool.specs[0]["description"] for tool in Tools.get_tools()
        }

        self.tools.update(featured_tools)

        self.tool_router = ToolRouter(
            tools=self.tools,
            model_name=self.valves.model,
            threshold=self.valves.threshold,
            top_n=self.valves.n,
        )
        print(f"Tools: {self.tool_router.candidates}")

        query = body["messages"][-1]["content"]
        selected_tools = self.tool_router.route_query(query)
        _tools_, prob = selected_tools[0] if selected_tools else (None, None)

        self.emitter.set_status_prefix("Tool Router: ")
        if _tools_ is None:
            await self.emitter.status(
                description="No tool selected",
                status="complete",
                done=True,
            )
        else:
            await self.emitter.status(
                description=f"Selected {_tools_} with probability {prob}",
                status="complete",
                done=True,
            )
        print("===" * 10)
        print(f"Selected tool: {_tools_}\nProbability: {prob}")
        print("===" * 10)

        # Only add to features and tool_ids if a valid tool was selected
        if _tools_ is not None:
            if _tools_ in featured_tools:
                body["features"][_tools_] = True
            body["tool_ids"] = [_tools_]
        else:
            # Handle the case where no tool was selected
            body["tool_ids"] = []

        return body

    def stream(self, event: dict) -> dict:
        return event

    async def outlet(self, body: dict) -> dict:
        return body
