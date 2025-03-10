import logging
import sys
from typing import Any, Dict, List, Tuple

from transformers import pipeline
from data import agents, tools

logging.disable(logging.CRITICAL)

class Router:
    def __init__(
        self,
        candidates: Dict[str, str],
        classifier: str = "zero-shot-classification",
        model: str = "facebook/bart-large-mnli",
        n: int = 1,
        threshold: float = 0.1,
    ) -> None:
        self.candidates: Dict[str, str] = candidates
        self.model: str = model
        self.classifier: Any = pipeline(classifier, model=model)
        self.n: int = n
        self.threshold: float = threshold

    def route_query(self, query: str) -> List[Tuple[str, float]]:
        candidate_values: List[str] = list(self.candidates.values())
        result: Dict[str, Any] = self.classifier(query, candidate_labels=candidate_values)
        logging.debug(result)
        
        description_to_name: Dict[str, str] = {desc: name for name, desc in self.candidates.items()}
        
        score_dict: Dict[str, float] = {
            description_to_name[label]: score
            for label, score in zip(result["labels"], result["scores"])
        }
        
        sorted_scores: List[Tuple[str, float]] = sorted(score_dict.items(), key=lambda item: item[1], reverse=True)
        filtered_scores: List[Tuple[str, float]] = [(k, v) for k, v in sorted_scores if v >= self.threshold]
        
        return filtered_scores[:self.n]

class AgentRouter(Router):
    def __init__(
        self,
        agents: Dict[str, str],
        classifier: str = "zero-shot-classification",
        model: str = "facebook/bart-large-mnli",
        n: int = 1,
        threshold: float = 0.1,
    ) -> None:
        super().__init__(agents, classifier, model, n, threshold)

class ToolRouter(Router):
    def __init__(
        self,
        tools: Dict[str, str],
        classifier: str = "zero-shot-classification",
        model: str = "facebook/bart-large-mnli",
        n: int = 3,
        threshold: float = 0.08,
    ) -> None:
        super().__init__(tools, classifier, model, n, threshold)

def main() -> None:
    agent_router: AgentRouter = AgentRouter(agents)
    tool_router: ToolRouter = ToolRouter(tools)

    query: str = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not query:
        query = input("Enter a query: ")

    selected_agent: List[Tuple[str, float]] = agent_router.route_query(query)
    selected_tools: List[Tuple[str, float]] = tool_router.route_query(query)

    print(f"Query: {query}")

    if selected_agent:
        print(f"Selected Agent: {selected_agent[0][0]} ({agents[selected_agent[0][0]]})")
    else:
        print("No agent selected.")

    if selected_tools:
        tools_str: str = ", ".join(tool for tool, score in selected_tools)
        print(f"Selected Tools: {tools_str}")
    else:
        print("No tools selected.")

if __name__ == '__main__':
    main()
