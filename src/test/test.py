import sys

from time import perf_counter
from typing import Set, Tuple, Dict, List
from dataclasses import dataclass
from datetime import datetime
from syn_data.data import test_data, agents, tools
from llm_routers import AgentRouter, ToolRouter
from testPlot import (
    plot_router_types_accuracy,
    plot_router_performance_by_type,
    plot_router_types_time_series,
    plot_router_types_summary
)

# Constants for router thresholds
AGENT_ROUTER_THRESHOLD = 0.1
TOOL_ROUTER_THRESHOLD = 0.1

@dataclass
class RouterResult:
    name: str
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    total: int = 0
    time: float = 0.0
    times: List[float] = None

    def __post_init__(self):
        self.times = [] 

    def add_time(self, time: float) -> None:
        self.time += time
        self.total += 1
        self.times.append(time)

    def get_avg_time(self) -> float:
        return self.time / self.total if self.total > 0 else 0

    def __str__(self) -> str:
        return (
            f"{self.name} Router Results:\n"
            f"  Passed: {self.passed} ✅\n"
            f"  Failed: {self.failed} ❌\n"
            f"  Warnings: {self.warnings} ⚠️\n"
            f"  Average Time: {self.get_avg_time():.6f}s"
        )

def validate_agent(selected: Tuple[str, float], expected: str, results: RouterResult) -> None:
    """Validate selected agent against expected agent."""
    if not selected:
        print("No agent selected. ❌")
        results.failed += 1
        return
    
    agent_name = selected[0][0]
    if agent_name == expected:
        print(f"Selected Agent: {agent_name} ({agents[agent_name]}) ✅")
        results.passed += 1
    else:
        print(f"Selected Agent: {agent_name} ({agents[agent_name]}) ❌ (Expected: {expected})")
        results.failed += 1

def validate_tools(selected: List[Tuple[str, float]], expected: Set[str], results: RouterResult) -> None:
    """Validate selected tools against expected tools."""
    if not selected:
        print("No tools selected. ❌")
        results.failed += 1
        return

    actual_tools = {tool for tool, _ in selected}
    extra_tools = actual_tools - expected
    missing_tools = expected - actual_tools
    
    if extra_tools or missing_tools:
        print(f"Selected Tools: {', '.join(actual_tools)} ❌")
        if missing_tools:
            print(f"Missing Tools: {', '.join(missing_tools)} ❌")
        if extra_tools:
            print(f"Extra Tools: {', '.join(extra_tools)} ❌")
        results.failed += 1
        if missing_tools:
            results.warnings += 1
        if extra_tools:
            results.warnings += 1
    else:
        print(f"Selected Tools: {', '.join(actual_tools)} ✅")
        results.passed += 1

def run_test(
    data_item: Dict, 
    routers: Tuple[AgentRouter, ToolRouter], 
    agent_results: RouterResult, 
    tool_results: RouterResult
) -> None:
    """Run single test with separate tracking for each router"""
    query = data_item["query"]
    agent_router, tool_router = routers
    
    # Time and validate agent selection
    start = perf_counter()
    selected_agent = agent_router.route_query(query)
    agent_time = perf_counter() - start
    agent_results.add_time(agent_time)
    
    # Time and validate tools selection
    start = perf_counter()
    selected_tools = tool_router.route_query(query)
    tools_time = perf_counter() - start
    tool_results.add_time(tools_time)
    
    print("\n" + "=" * 50)
    print(f"Query: {query}")
    
    # Validate results
    validate_agent(selected_agent, data_item["expected_agent"], agent_results)
    validate_tools(selected_tools, set(data_item["expected_tools"]), tool_results)

def test_route_query() -> None:
    """Main test function with separated router results and plotting by router type"""
    # Initialize test components
    router_results = {
        'AgentRouter': RouterResult("AgentRouter"),
        'ToolRouter': RouterResult("ToolRouter"),
        # Add more router types as needed
    }
    
    agent_router = AgentRouter(agents, 
                                model_name="facebook/bart-large-mnli",
                                top_n=1,
                                threshold=AGENT_ROUTER_THRESHOLD)
    tool_router = ToolRouter(tools,
                                model_name="facebook/bart-large-mnli",
                                top_n=3,
                                threshold=TOOL_ROUTER_THRESHOLD)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for data_item in test_data:
        query = data_item["query"]
        
        # Test AgentRouter
        start = perf_counter()
        selected_agent = agent_router.route_query(query)
        agent_time = perf_counter() - start
        router_results['AgentRouter'].add_time(agent_time)
        
        # Test ToolRouter
        start = perf_counter()
        selected_tools = tool_router.route_query(query)
        tool_time = perf_counter() - start
        router_results['ToolRouter'].add_time(tool_time)
        
        print("\n" + "=" * 50)
        print(f"Query: {query}")
        
        # Validate results
        validate_agent(selected_agent, data_item["expected_agent"], router_results['AgentRouter'])
        validate_tools(selected_tools, set(data_item["expected_tools"]), router_results['ToolRouter'])
    
    # Print summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("-" * 20)
    print(f"Total Test Cases: {len(test_data)}")
    for router_name, results in router_results.items():
        print("\n" + str(results))
    
    router_times = {
        name: results.times 
        for name, results in router_results.items()
    }
    
    # Generate plots
    plot_router_performance_by_type(router_times, timestamp)
    plot_router_types_accuracy(router_results, timestamp)
    plot_router_types_time_series(router_times, timestamp)
    plot_router_types_summary(router_results, timestamp)
    
    print("\nPlots have been saved in the 'plots' directory.")



if __name__ == "__main__":
    test_route_query()