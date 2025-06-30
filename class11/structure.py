import os

def create_project_structure(base_path="knowledge_graph_builder"):
    folders = [
        base_path,
        f"{base_path}/agents",
        f"{base_path}/tools",
        f"{base_path}/workflows",
        f"{base_path}/utils",
        f"{base_path}/data",
        f"{base_path}/data/outputs"
    ]

    files = {
        f"{base_path}/app.py": """from agents.researcher import Researcher
from workflows.langgraph_router import LangGraphRouter

def main():
    print("🚀 Knowledge Graph Builder Starting...")
    researcher = Researcher()
    router = LangGraphRouter()
    # router.run()  # Uncomment when implemented

if __name__ == "__main__":
    main()
""",

        f"{base_path}/agents/__init__.py": "# agents package",
        f"{base_path}/agents/researcher.py": "# Researcher agent logic here",
        f"{base_path}/agents/synthesizer.py": "# Synthesizer agent logic here",
        f"{base_path}/agents/mapper.py": "# Mapper agent logic here",

        f"{base_path}/tools/__init__.py": "# tools package",
        f"{base_path}/tools/serpapi_tool.py": "# SERPAPI integration",
        f"{base_path}/tools/wikipedia_tool.py": "# Wikipedia API wrapper",
        f"{base_path}/tools/research_api_tool.py": "# Custom research tool logic",

        f"{base_path}/workflows/__init__.py": "# workflows package",
        f"{base_path}/workflows/langgraph_router.py": "# LangGraph decision router logic",

        f"{base_path}/utils/__init__.py": "# utils package",
        f"{base_path}/utils/graphviz_exporter.py": "# GraphViz export logic",
        f"{base_path}/utils/config.py": """# Configurations
SERPAPI_KEY = 'your-serpapi-key-here'
WIKIPEDIA_API_ENDPOINT = 'https://en.wikipedia.org/w/api.php'
""",
        f"{base_path}/utils/logger.py": """import logging

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(ch)
    return logger
""",

        f"{base_path}/requirements.txt": """openai
langchain
graphviz
wikipedia
requests
serpapi
""",

     f"{base_path}/README.md": """# Knowledge Graph Builder 🧠🔗

# This project aims to build a knowledge graph using various agents and tools, integrating data from multiple sources.
"""
    }

    # Create folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # Create files
    for file_path, content in files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    create_project_structure()


print("Folder structure created successfully.")
# This script creates a folder structure for a knowledge graph builder project.    