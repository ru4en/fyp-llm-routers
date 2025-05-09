import os
import matplotlib.pyplot as plt
import seaborn as sns
import csv

def save_router_test_plot(
    agent_passes, agent_warnings, agent_fails,
    tool_passes, tool_warnings, tool_fails,
    agent_results_list, tool_results_list,
    tool_stats,
    agent_stats,
    total_tests,
    outdir="plots"
):
    os.makedirs(outdir, exist_ok=True)
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("Router Test Results (Agents and Tools)", fontsize=18, fontweight='bold')

    # AGENT ROUTER BAR
    agent_counts = [agent_passes, agent_warnings, agent_fails]
    agent_labels = ["PASS", "WARNING", "FAIL"]
    agent_colors = ["#4caf50", "#ffb300", "#e53935"]
    sns.barplot(x=agent_labels, y=agent_counts, ax=axes[0], palette=agent_colors)
    axes[0].set_title("Agent Router", fontsize=14)
    axes[0].set_ylabel("Count")
    axes[0].set_xlabel("Result")
    axes[0].set_ylim(0, max(agent_counts + [tool_passes, tool_warnings, tool_fails]) + 2)
    for i, v in enumerate(agent_counts):
        axes[0].text(i, v + 0.1, str(v), color='black', ha='center', fontsize=12, fontweight='bold')

    # TOOL ROUTER BAR
    tool_counts = [tool_passes, tool_warnings, tool_fails]
    tool_labels = ["PASS", "WARNING", "FAIL"]
    tool_colors = ["#4caf50", "#ffb300", "#e53935"]
    sns.barplot(x=tool_labels, y=tool_counts, ax=axes[1], palette=tool_colors)
    axes[1].set_title("Tool Router", fontsize=14)
    axes[1].set_ylabel("Count")
    axes[1].set_xlabel("Result")
    axes[1].set_ylim(0, max(tool_counts + [agent_passes, agent_warnings, agent_fails]) + 2)
    for i, v in enumerate(tool_counts):
        axes[1].text(i, v + 0.1, str(v), color='black', ha='center', fontsize=12, fontweight='bold')

    plt.tight_layout(rect=[0, 0.03, 1, 0.92])
    plt.savefig(os.path.join(outdir, "router_test_summary.png"))
    plt.close(fig)

    # TOOL STATS PLOT
    plt.figure(figsize=(max(8, len(tool_stats)*0.5), 6))
    tool_names = list(tool_stats.keys())
    tool_pass = [tool_stats[k]['pass'] for k in tool_names]
    tool_warn = [tool_stats[k]['warning'] for k in tool_names]
    tool_fail = [tool_stats[k]['fail'] for k in tool_names]
    bar_width = 0.35

    idx = range(len(tool_names))
    plt.bar(idx, tool_pass, bar_width, label='PASS', color="#4caf50")
    plt.bar(idx, tool_warn, bar_width, bottom=tool_pass, label='WARNING', color="#ffb300")
    plt.bar(idx, tool_fail, bar_width, bottom=[tool_pass[i] + tool_warn[i] for i in idx], label='FAIL', color="#e53935")
    plt.xticks(idx, tool_names, rotation=45, ha='right', fontsize=10)
    plt.ylabel("Count")
    plt.title("Tool Routing: Correct / Warning / Wrong by Tool", fontsize=16)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "tool_routing_per_tool.png"))
    plt.close()

    # AGENT STATS PLOT
    plt.figure(figsize=(max(8, len(agent_stats)*0.5), 6))
    agent_names = list(agent_stats.keys())
    agent_pass = [agent_stats[k]['pass'] for k in agent_names]
    agent_warn = [agent_stats[k]['warning'] for k in agent_names]
    agent_fail = [agent_stats[k]['fail'] for k in agent_names]

    idx = range(len(agent_names))
    plt.bar(idx, agent_pass, bar_width, label='PASS', color="#4caf50")
    plt.bar(idx, agent_warn, bar_width, bottom=agent_pass, label='WARNING', color="#ffb300")
    plt.bar(idx, agent_fail, bar_width, bottom=[agent_pass[i] + agent_warn[i] for i in idx], label='FAIL', color="#e53935")
    plt.xticks(idx, agent_names, rotation=45, ha='right', fontsize=10)
    plt.ylabel("Count")
    plt.title("Agent Routing: Correct / Warning / Wrong by Agent", fontsize=16)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "agent_routing_per_agent.png"))
    plt.close()

    print(f"Plots saved to {outdir}/")

def test_agent_router():
    from llm_routers import AgentRouter, ToolRouter
    from syn_data.data import agents as AGENTS, tools as TOOLS, test_data

    total_tests = len(test_data)
    agent_passes = 0
    agent_warnings = 0
    agent_fails = 0
    tool_passes = 0
    tool_warnings = 0
    tool_fails = 0

    agent_results_list = []
    tool_results_list = []

    tool_stats = {k: {'pass': 0, 'warning': 0, 'fail': 0} for k in TOOLS}
    agent_stats = {k: {'pass': 0, 'warning': 0, 'fail': 0} for k in AGENTS}

    # Initialize routers
    try:
        agent_router = AgentRouter(
            agents=AGENTS,
            model_name="routellm/bert_mmlu_augmented",
            top_n=3,
            threshold=0.08,
            fallback_on_error=False,
        )
        tool_router = ToolRouter(
            tools=TOOLS,
            model_name="routellm/bert_mmlu_augmented",
            top_n=3,
            threshold=0.08,
            fallback_on_error=False,
        )
    except Exception as e:
        print(f"Router initialisation failed - {str(e)}")
        return

    # Run tests
    for i, prompt in enumerate(test_data):
        query = prompt.get("query", "")
        expected_agent = prompt.get("expected_agent", "")
        expected_tools = prompt.get("expected_tools", [])

        # Test agent router
        try:
            agent_results = agent_router.route_query(query)
            agent_found = False
            top_match = False
            for idx, (agent_name, score) in enumerate(agent_results):
                if agent_name == expected_agent:
                    agent_found = True
                    if idx == 0:
                        top_match = True
            if top_match:
                agent_passes += 1
                agent_results_list.append("PASS")
                if expected_agent in agent_stats:
                    agent_stats[expected_agent]['pass'] += 1
            elif agent_found:
                agent_warnings += 1
                agent_results_list.append("WARNING")
                if expected_agent in agent_stats:
                    agent_stats[expected_agent]['warning'] += 1
            else:
                agent_fails += 1
                agent_results_list.append("FAIL")
                if expected_agent in agent_stats:
                    agent_stats[expected_agent]['fail'] += 1
        except Exception as e:
            agent_fails += 1
            agent_results_list.append("FAIL")
            if expected_agent in agent_stats:
                agent_stats[expected_agent]['fail'] += 1

        # Test tool router
        try:
            tool_results = tool_router.route_query(query)
            found_tools = []
            for tool_name, score in tool_results:
                if tool_name in expected_tools:
                    found_tools.append(tool_name)
            missing_tools = [t for t in expected_tools if t not in found_tools]

            # Stats per-tool
            # Mark as pass/warning/fail per expected tool
            if set(found_tools) == set(expected_tools):
                tool_passes += 1
                tool_results_list.append("PASS")
                for t in found_tools:
                    tool_stats[t]['pass'] += 1
            elif found_tools and missing_tools:
                tool_warnings += 1
                tool_results_list.append("WARNING")
                for t in found_tools:
                    tool_stats[t]['warning'] += 1
                for t in missing_tools:
                    tool_stats[t]['fail'] += 1
            else:
                tool_fails += 1
                tool_results_list.append("FAIL")
                for t in expected_tools:
                    tool_stats[t]['fail'] += 1
        except Exception as e:
            tool_fails += 1
            tool_results_list.append("FAIL")
            for t in prompt.get("expected_tools", []):
                tool_stats[t]['fail'] += 1

    # Print summary
    print("\n===== TEST SUMMARY =====")
    print(f"Total tests: {total_tests}")
    print(f"Agent router results: PASS={agent_passes}, WARNING={agent_warnings}, FAIL={agent_fails}")
    print(f"Tool router results:  PASS={tool_passes}, WARNING={tool_warnings}, FAIL={tool_fails}")

    # Save plots
    save_router_test_plot(
        agent_passes, agent_warnings, agent_fails,
        tool_passes, tool_warnings, tool_fails,
        agent_results_list, tool_results_list,
        tool_stats,
        agent_stats,
        total_tests,
        outdir="plots"
    )

    # Export summary to CSV
    with open("test_summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "PASS", "WARNING", "FAIL"])
        writer.writerow(["Agent Router", agent_passes, agent_warnings, agent_fails])
        writer.writerow(["Tool Router", tool_passes, tool_warnings, tool_fails])

    # Export agent stats to CSV
    with open("agent_stats.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Agent", "PASS", "WARNING", "FAIL"])
        for agent_name, stats in agent_stats.items():
            writer.writerow([agent_name, stats['pass'], stats['warning'], stats['fail']])

    # Export tool stats to CSV
    with open("tool_stats.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Tool", "PASS", "WARNING", "FAIL"])
        for tool_name, stats in tool_stats.items():
            writer.writerow([tool_name, stats['pass'], stats['warning'], stats['fail']])
    # Cleanup
    try:
        agent_router.shutdown()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    test_agent_router()