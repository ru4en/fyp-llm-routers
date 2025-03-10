from data import test_data

def test_route_query():
    from main import AgentRouter, ToolRouter
    from data import agents, tools

    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    warnings_count = 0

    for data_item in test_data:
        total_tests += 1
        query = data_item["query"]
        expected_agent = data_item["expected_agent"]
        expected_tools = set(data_item["expected_tools"])  # use a set for easier comparison

        agent_router = AgentRouter(agents)
        tool_router = ToolRouter(tools)

        selected_agent = agent_router.route_query(query)
        selected_tools = tool_router.route_query(query)

        print("=" * 50)
        print(f"Query: {query}")

        test_passed = True

        # Check selected agent
        if selected_agent:
            agent_name = selected_agent[0][0]
            if agent_name == expected_agent:
                print(f"Selected Agent: {agent_name} ({agents[agent_name]}) ✅")
            else:
                print(f"Selected Agent: {agent_name} ({agents[agent_name]}) ❌ (Expected: {expected_agent})")
                test_passed = False
        else:
            print("No agent selected. ❌")
            test_passed = False

        # Check selected tools
        if selected_tools:
            actual_tools = {tool for tool, score in selected_tools}
            extra_tools = actual_tools - expected_tools
            missing_tools = expected_tools - actual_tools

            if extra_tools:
                print(f"Selected Tools: {', '.join(actual_tools)} ❌ (Unexpected tool(s): {', '.join(extra_tools)})")
                test_passed = False
            else:
                if missing_tools:
                    print(f"Selected Tools: {', '.join(actual_tools)} ⚠️ (Missing tool(s): {', '.join(missing_tools)})")
                    warnings_count += 1
                else:
                    print(f"Selected Tools: {', '.join(actual_tools)} ✅")
        else:
            print("No tools selected. ❌")
            test_passed = False

        if test_passed:
            passed_tests += 1
        else:
            failed_tests += 1

    print("=" * 50)
    print(f"Total tests: {total_tests}, Passed: {passed_tests} ✅, Failed: {failed_tests} ❌, Warnings: {warnings_count} ⚠️")

if __name__ == "__main__":
    test_route_query()
