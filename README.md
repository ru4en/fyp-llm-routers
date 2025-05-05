

# Routers for LLM: A Framework for Model Selection and Tool Invocation

> ## Final year project
> Author: *Ruben J. Lopes*  \
> Date: *2025-05-04*  \
> Supervised by: *Dr Xiaomin Chen*  \
> FYP GitHub: *[ru4en/fyp-llm-routers](https://github.com/ru4en/fyp-llm-routers)*
> Library GitHub: *[ru4en/llm-routers](https://github.com/ru4en/llm-routers)*
> Website: *[fyp.rubenlopes.uk](https://fyp.rubenlopes.uk)*
> Poster: *[fyp.rubenlopes.uk/poster](https://fyp.rubenlopes.uk/poster)*
---

## Introduction

Routers for LLM is a framework for model selection and tool invocation. Its an interface for LLMs tools to easily use NLI (Natural Language Interface) to select the best model for a given task and invoke the appropriate tool. The framework is designed to be extensible and easy to use, allowing developers to add new models and tools as needed.

## Directories

### Documentation

- `docs/poster`: poster for the final year project.
- `docs/presentation`: presentation slides.
- `docs/report`: Contains the report.
- `docs/website`: Contains the website sources.


### Models
- `models/llm_routers`: Contains the fine-tuned models for the framework.

### Sources
- `src/llm_routers`: Contains the main code for the framework.
- `src/training`: Contains the jupyter notebooks that were used to train the models.

- `src/test/demo.py`: runs the demo to interact with the framework using a CLI.

- `src/test/test.py`: runs the tests for the framework using synctactic data.

- `src/openwebui-plugins`: Contains the plugins to use this library with openwebui.


## Installation

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Requirements

- Python 3.11 or higher


## Useage

### Trying out the demo

```
python src/test/demo.py
```

### Running the tests
```bash
python src/test/test.py

```

### Trying out the Demo

1. Clone the repository
```bash
python src/test/demo.py
```


### Using OpenWebUI Plugin

1. Start a local instance of OpenWebUI or requst Ruben credentials to use the test instance.

2. From `src/plugins/exports` download the `agent-router.json` and `tool-router.json` files.

3. Go to the OpenWebUI instance and click on Admin Panel > Functions > Import Function.
4. Select the `<*>-router.json` files and click on Import.

> To use the tool router, simply select a model and a tool from the dropdown menus. The tool router will automatically select the best model for the given task and invoke the appropriate tool.

> For the agent router, select the `🧠 Auto Agent Router` and ask it a query. The agent router will automatically select the best agent for the given task.



### Using the Library
```python
from llm_routers import AgentRouter, ToolRouter, Router

# Create an agent router

AGENTS = [
        {"agent": "This is agent 1"},
        {"agent2": "This is agent 2"},
        {"agent3": "This is agent 3"}
]

TOOLS = [
        {"tool": "This is tool 1"},
        {"tool2": "This is tool 2"},
        {"tool3": "This is tool 3"}
]

# Create an agent router
agent_router = AgentRouter(
    agents=AGENTS,
    model_name="ru4en/bart-large-mnli-agent-router-v2",
    top_n=3,
    threshold=0.01,
    verbose=True
)

# Create a tool router
tool_router = ToolRouter(
    tools=TOOLS,
    model_name="ru4en/bart-large-mnli-tool-router-v2",
    top_n=3,
    threshold=0.01,
    verbose=True
)

# Route the input to the appropriate agent
input = "This is the input"
agent = agent_router.route_query(input)
print(f"Agent: {agent}")

# Route the input to the appropriate tool
tools = tool_router.route_query(input)
print(f"Tools: {tools}")

```
