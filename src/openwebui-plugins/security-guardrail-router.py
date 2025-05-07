"""
title: Security Guardrail Router
author: Ruben Lopes (@ru4en)
version: 0.2
"""

import logging
from typing import Dict, List, Optional, Tuple, Callable, Any, Awaitable
from pydantic import BaseModel, Field, validator
from llm_routers import Router
from datetime import datetime
import inspect
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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


class SecurityTask(BaseModel):
    """Model for security tasks with validation"""

    attack: str
    description: str

    @validator("attack")
    def validate_attack_name(cls, v):
        if not v.strip():
            raise ValueError("Attack name cannot be empty")
        return v


# Predefined security tasks
SECURITY_TASKS = [
    SecurityTask(
        attack="Prompt Injection",
        description="Attacks that manipulate the model's behavior by injecting malicious prompts.",
    ),
    SecurityTask(
        attack="Data Leakage",
        description="Attacks that extract sensitive information from the model's training data.",
    ),
    SecurityTask(
        attack="Model Evasion",
        description="Attacks that bypass the model's security measures.",
    ),
    SecurityTask(
        attack="Adversarial Examples",
        description="Attacks that use specially crafted inputs to mislead the model.",
    ),
    SecurityTask(
        attack="Malicious Code",
        description="Attacks that inject harmful code into the model's responses.",
    ),
    SecurityTask(
        attack="Malicious Query",
        description="Attacks that use harmful queries that could cause harm.",
    ),
]


class SecurityValves(BaseModel):
    """Configuration model for security routing"""

    model: str = Field(
        "facebook/bart-large-mnli",
        description="The model to use for the zero-shot classification task.",
    )
    n: int = Field(3, description="The number of models to return.", ge=1, le=10)
    threshold: float = Field(
        0.08, description="The threshold for model selection.", ge=0.0, le=1.0
    )
    classification: List[SecurityTask] = Field(
        default=SECURITY_TASKS,
        description="A list of security tasks and their descriptions.",
    )


class Pipe:
    """
    A security-focused router that analyzes incoming queries for potential security risks
    and routes them to appropriate handlers.
    """

    def __init__(self):
        """Initialize the security guardrail with default configuration"""
        self.valves = SecurityValves()
        self.classifier = None
        self._initialize_time = datetime.utcnow().isoformat()

    def _lazy_init_classifier(self) -> None:
        """Lazily initialize the classifier when needed"""
        if self.classifier is None:
            try:
                self.classifier = Router(
                    candidates={
                        task.attack: task.description
                        for task in self.valves.classification
                    },
                    model_name=self.valves.model,
                    top_n=0.1,
                    threshold=self.valves.threshold,
                )
                logging.info("Security classifier initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize security classifier: {e}")
                raise RuntimeError(f"Classifier initialization failed: {e}")

    def _extract_query(self, body: dict) -> Optional[str]:
        """Extract the latest user query from the message body"""
        if not isinstance(body, dict):
            logging.warning("Invalid body format: expected dictionary")
            return None

        if "messages" not in body or not isinstance(body["messages"], list):
            logging.warning("No messages found in body")
            return None

        for msg in reversed(body["messages"]):
            if (
                isinstance(msg, dict)
                and msg.get("role") == "user"
                and isinstance(msg.get("content"), str)
            ):
                return msg["content"].strip()

        return None

    def analyze_security(self, query: str) -> List[Tuple[str, float]]:
        """
        Analyze the security implications of a query.

        Args:
            query: The user's input query

        Returns:
            List of (attack_type, confidence_score) tuples
        """
        self._lazy_init_classifier()

        try:
            results = self.classifier.route_query(query)
            if results:
                logging.info(
                    f"Security analysis complete - Found {len(results)} potential risks"
                )
                return results
            logging.info("No security risks detected")
            return []

        except Exception as e:
            logging.error(f"Security analysis failed: {e}")
            return []

    async def pipe(
        self,
        body: dict,
        __event_emitter__: Optional[Callable[[dict], Awaitable[None]]] = None,
    ) -> dict:
        """
        Process incoming messages through security analysis.

        Args:
            body: The message body containing the query

        Returns:
            Processed body with security analysis results
        """
        self.emitter = EventEmitter(__event_emitter__)
        await self.emitter.status(
            "Analyzing security...", status="in_progress", done=False
        )
        query = self._extract_query(body)
        if not query:
            return {
                "error": "No valid query found in message body",
                "original_body": body,
            }

        security_results = self.analyze_security(query)

        await self.emitter.status(
            description="Security analysis complete",
            status="complete",
            done=True,
        )

        if security_results:
            body["security_analysis"] = {
                "query": query,
                "results": [
                    {"attack_type": attack, "confidence_score": score}
                    for attack, score in security_results
                ],
            }
            logging.info(f"Security analysis results: {body['security_analysis']}")
        else:
            body["security_analysis"] = {
                "query": query,
                "results": [],
            }
            logging.info("No security risks detected")
        return f"""
SECURITY ANALYSIS RESULTS:
{security_results}
        """

    def pipes(self) -> List[Dict]:
        return [
            {
                "id": "security_guardrail",
                "name": "🛡️ Security Guardrail",
                "description": "Analyzes queries for potential security risks",
                "version": "0.2",
                "initialized": self._initialize_time,
            }
        ]
