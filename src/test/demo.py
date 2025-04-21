TOOLS = {
    "calculator": "A calculator that can add, subtract, multiply and divide.",
    "python": "A Python interpreter that can run Python code.",
    "web_browser": "A web browser that can browse the web.",
    "terminal": "A terminal that can run shell commands.",
    "email": "An email client that can send and receive emails.",
    "calendar": "A calendar that can manage events and reminders.",
    "notes_app": "A notes application that can take and organise notes.",
    "spreadsheet": "A spreadsheet that can perform calculations and data analysis.",
    "text_editor": "A text editor that can edit text files.",
    "code_interpreter": "A code interpreter that can run code in various languages.",
    "image_generation": "An image generation tool that can generate images based on text prompts.",
    "text_summarizer": "A text summariser that can summarise long texts into shorter versions.",
    "text_translation": "A text translation tool that can translate text from one language to another.",
    "text_generation": "A text generation tool that can generate text based on prompts.",
    "text_classification": "A text classification tool that can classify text into different categories.",
    "text_analysis": "A text analysis tool that can analyse text for sentiment, keywords, etc.",
    "text_to_speech": "A text-to-speech tool that can convert text into speech.",
    "speech_to_text": "A speech-to-text tool that can convert speech into text.",
    "text_to_image": "A text-to-image tool that can generate images from text descriptions."
}

COMPLEXITY = {
    "simple": "A simple task that requires basic understanding.",
    "complex": "A complex task that requires advanced understanding."
}

AGENTS = {
    "Adam": "A Python developer who can write and debug Python code.",
    "Eve": "A graphic designer who can create and edit images.",
    "Charlie": "A data analyst who can analyse and visualise data.",
    "Grace": "A project manager who can manage tasks and schedules.",
    "Sophia": "A customer support agent who can respond to customer queries."
}

from llm_routers import Router, AgentRouter, ToolRouter
import os
import sys
import signal
import logging
logging.basicConfig(level=logging.ERROR)

# Suppress HuggingFace warnings
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Change these lines in demo.py
agent_router = AgentRouter(
    agents=AGENTS,
    model_name="facebook/bart-large-mnli",
    top_n=3,
    threshold=0.1,
    async_mode=False,
    device="cpu",
)

tool_router = ToolRouter(
    tools=TOOLS,
    model_name="facebook/bart-large-mnli",
    top_n=3,
    threshold=0.1,
    async_mode=False,
    device="cpu",
)

complexity_router = Router(
    candidates=COMPLEXITY,
    model_name="facebook/bart-large-mnli",
    top_n=1,
    threshold=0.1,
    pipeline_name="zero-shot-classification",
    async_mode=False,
    device="cpu",
)

def signal_handler(sig, frame):
    print("\nExiting gracefully...")
    agent_router.shutdown()
    tool_router.shutdown()
    complexity_router.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    while True:
        prompt = input("Enter the prompt: ").strip()
        if prompt.lower() in {"exit", "quit", "q"}:
            break

        agents = agent_router.route_query(prompt)
        tools = tool_router.route_query(prompt)
        complexity = complexity_router.route_query(prompt)
        
        print(f"\n\tAGENTS:")
        for agent_name, score in agents:
            print(f"\t\t- {agent_name}: {score:.2f} - {AGENTS[agent_name]}")
            
        print(f"\n\tTOOLS:")
        for tool_name, score in tools:
            print(f"\t\t- {tool_name}: {score:.2f}")
            
        print(f"\n\tCOMPLEXITY:")
        for complexity_name, score in complexity:
            print(f"\t\t- {complexity_name}: {score:.2f}")

        print("-" * 40)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    agent_router.shutdown()
    tool_router.shutdown()
    complexity_router.shutdown()