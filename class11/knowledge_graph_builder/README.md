# Learning Resource Knowledge Graph Builder 🧠📚🔗

A multi-agent system that builds comprehensive learning resource collections and knowledge graphs on any topic using AI. This project helps learners find the best resources across different platforms, organize them into a structured learning path, and visualize the relationships between concepts.

## Features

- **Multi-Agent Architecture**: Researcher, Synthesizer, and Mapper agents work together to create comprehensive learning resources and knowledge graphs
- **Multiple Data Sources**: Integrates Google Search, Wikipedia, YouTube videos, online courses, and book recommendations
- **Learning Resource Curation**: Identifies and organizes the best learning materials for any topic
- **Learning Path Generation**: Creates structured learning paths from beginner to advanced
- **Interactive Visualization**: Generates SVG knowledge graphs with clear relationships between concepts
- **Resource Categorization**: Organizes materials by type (videos, courses, books, web resources)
- **API Backend**: FastAPI backend for programmatic access
- **React Frontend**: Modern UI for interacting with the knowledge graph system
- **Streamlit UI**: Simple, intuitive, and responsive user interface with tabbed resource views

## Project Structure

```
knowledge_graph_builder/
├── agents/               # Agent logic
│   ├── researcher.py     # Gathers information and learning resources from various sources
│   ├── synthesizer.py    # Processes and structures the information into learning paths
│   └── mapper.py         # Creates the knowledge graph structure
├── tools/                # External API integrations
│   ├── serpapi_tool.py   # Google Search integration
│   ├── wikipedia_tool.py # Wikipedia API wrapper
│   ├── research_api_tool.py # Custom research tool
│   └── youtube_tool.py   # YouTube video search (simulated)
├── workflows/            # Orchestration logic
│   └── langgraph_router.py # LangGraph decision router
├── utils/                # Utility functions
│   ├── graphviz_exporter.py # SVG export functionality
│   ├── config.py         # Configuration settings
│   └── logger.py         # Logging utilities
├── app.py               # Streamlit UI application with tabbed resource views
├── .env                 # Environment variables and API keys
└── requirements.txt     # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Graphviz (for visualization)
- API keys for:
  - EURI API (for AI completions)
  - SERP API (for Google search results)
  - YouTube API (optional, for video search)

### Installation

1. Clone the repository
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env` file:
   ```
   SERPAPI_API_KEY=your_serpapi_key
   EURI_API_KEY=your_euri_api_key
   YOUTUBE_API_KEY=your_youtube_api_key  # Optional, for video search
   ```

### Running the Application

#### Streamlit UI

```bash
cd knowledge_graph_builder
streamlit run app.py
```

#### FastAPI Backend

```bash
cd backend
uvicorn main:app --reload
```

#### React Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `POST /run`: Start a knowledge graph and learning resource generation job
- `GET /status/{job_id}`: Check job status
- `GET /result/{job_id}`: Get job results (knowledge graph and learning resources)
- `GET /resources/{job_id}`: Get curated learning resources for a specific job
- `GET /courses/{job_id}`: Get recommended online courses for a specific job
- `GET /videos/{job_id}`: Get recommended YouTube videos for a specific job
- `GET /books/{job_id}`: Get recommended books for a specific job
- `GET /download/{job_id}`: Download SVG file of the knowledge graph

## Learning Resources Feature

The Learning Resource Knowledge Graph Builder helps you find and organize the best educational materials on any topic:

- **Comprehensive Resource Search**: Finds relevant learning materials from multiple platforms including Google, YouTube, online course providers, and book recommendations

- **Resource Categorization**: Organizes materials by type (videos, courses, books, web resources) for easy navigation

- **Learning Path Generation**: Creates a structured learning path from beginner to advanced levels

- **Prerequisites Identification**: Identifies foundational knowledge needed before tackling the main topic

- **Practical Applications**: Suggests real-world applications and projects to reinforce learning

- **Visual Knowledge Graph**: Visualizes relationships between concepts for better understanding

- **Tabbed Interface**: Easy-to-navigate UI with separate tabs for different resource types

## Usage Examples

Try generating learning resources for topics like:

- "Machine Learning for Beginners"
- "Web Development with React"
- "Python Data Science"
- "Quantum Computing Basics"
- "Digital Marketing Strategies"

## License

MIT
