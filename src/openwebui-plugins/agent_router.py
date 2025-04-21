"""
title: Agent Router
author: Ruben Lopes (@ru4en)
description: |
  This is a simple agent router that uses a zero-shot classification model to route queries to the appropriate agent or tool.
  It uses the Hugging Face Transformers library for the zero-shot classification model.
  The router can be used to route queries to different agents or tools based on their descriptions.
  The router can be used in a pipeline with other components.
requirements: pydantic, requests, git+https://github.com/ru4en/llm_routers.git
version: 1.0.0
"""

from llm_routers import AgentRouter
from pydantic import BaseModel, Field
import logging
from typing import (
    Union,
    Generator,
    Iterator,
    List,
    Dict,
    Optional,
    Callable,
    Awaitable,
    Any,
    Tuple,
)

from transformers import pipeline

tasklist = [
    {
        "model": "Email Assistant",
        "tasks": "Generate email responses, summarize emails, extract information from emails",
    },
    {
        "model": "Code Assistant",
        "tasks": "Generate code snippets, debug code, explain code functionality",
    },
    {
        "model": "Text Summarizer",
        "tasks": "Summarize long texts, extract key points from articles, create concise summaries",
    },
    {
        "model": "Chatbot",
        "tasks": "Engage in conversation, answer questions, provide information",
    },
    {
        "model": "Sentiment Analysis",
        "tasks": "Analyze sentiment of text, classify text as positive/negative/neutral",
    },
]


def generate_chat_completion(query: str) -> str:
    """
    Simulate a chat completion response for the given query.
    This is a placeholder function and should be replaced with actual logic.
    """
    # Simulated response
    return f"Simulated response for query: {query}"


class Pipe:
    class Valves(BaseModel):
        model: str = Field(
            "facebook/bart-large-mnli",
            description="The model to use for the zero-shot classification task.",
        )
        n: int = Field(3, description="The number of models to return.")
        threshold: float = Field(0.08, description="The threshold for model selection.")
        classification: List[Dict[str, str]] = Field(
            tasklist,
            description="A list of models and their associated tasks.",
        )

    def __init__(self):
        self.valves = self.Valves()
        self.classifier = None
        # Initialize the classifier only when needed to avoid loading it at startup

    def pipe(self, body: dict):
        """
        Process the incoming request by routing to the best model.

        This function:
        1. Extracts the user query from the body
        2. Routes the query to find the best matching model
        3. Updates the body with the selected model ID
        4. Returns the updated body

        Args:
            body: Input data containing the user query

        Returns:
            Updated body with the selected model ID
        """
        try:
            # Extract the user query from messages
            query = ""
            if "messages" in body and len(body["messages"]) > 0:
                # Get the most recent user message
                for msg in reversed(body["messages"]):
                    if msg.get("role") == "user" and "content" in msg:
                        query = msg["content"]
                        break

            if not query:
                logging.warning("No user query found in the request")
                return body  # Return original body if no query found

            if self.classifier is None:
                self.classifier = AgentRouter(
                    agents={
                        task["model"]: task["tasks"]
                        for task in self.valves.classification
                    },
                    model_name=self.valves.model,
                    top_n=self.valves.n,
                    threshold=self.valves.threshold,
                )

            # Log the incoming query
            logging.debug(f"Incoming query: {query}")
            # Route the query to find the best matching model
            results = self.classifier.route_query(query)
            logging.debug(f"Routing results: {results}")

            if results:
                # Get the best model ID (highest score)
                best_model_id, score = results[0]
                logging.info(
                    f"Selected model '{best_model_id}' with confidence {score:.4f} for query: {query[:50]}..."
                )

                # Update the body with the selected model
                body["model"] = best_model_id

                # Optionally add routing info to the body for transparency
                body["_routing"] = {
                    "selected_model": best_model_id,
                    "confidence": score,
                    "all_matches": [
                        {"model": model, "score": round(score, 4)}
                        for model, score in results
                    ],
                }
            else:
                logging.warning(f"No suitable model found for query: {query[:50]}...")

            response = generate_chat_completion(query)
            return f"""
            {body.get('model', 'No model selected')}: {response}
            Agent Router Pipe Debug Info:
            ==========================
            Query: {query}
            Selected Agent: {body.get('model')}
            Tools: {body.get('tools')}
            Confidence: {body.get('_routing', {}).get('confidence')}
            All Matches: {body.get('_routing', {}).get('all_matches')}
            Response: {response}
            ==========================
            """

        except Exception as e:
            logging.error(f"Error in model router pipe: {e}")
            # Return original body on error
            return f"""
            Error in model router pipe: {e}
            Please check the logs for more details.
            
            body: {body}
            """

    def pipes(self):
        """
        Generate the list of models for the Open WebUI interface.

        Returns:
            List of dictionaries with model information
        """
        model_router_info = {
            "id": "model_router",
            "name": "🧠 Auto Agent Router",
            "description": "Automatically selects the best model for your task",
        }

        # Return the router as a single model option
        return [model_router_info]
