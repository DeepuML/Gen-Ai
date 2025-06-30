# Knowledge Graph Builder Project

A full-stack application for generating AI-powered knowledge graphs on any topic. This project consists of three main components:

1. **Knowledge Graph Builder**: Core Python library with multi-agent architecture
2. **FastAPI Backend**: API service for knowledge graph generation
3. **React Frontend**: Modern web interface for interacting with the system

## Project Structure

```
├── knowledge_graph_builder/  # Core Python library
│   ├── agents/              # Agent logic
│   ├── tools/               # External API integrations
│   ├── workflows/           # Orchestration logic
│   ├── utils/               # Utility functions
│   ├── app.py               # Streamlit UI
│   └── requirements.txt     # Python dependencies
├── backend/                 # FastAPI backend
│   └── main.py              # API endpoints
└── frontend/                # React frontend
    ├── src/                 # React components
    ├── public/              # Static assets
    └── package.json         # Node.js dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Graphviz (for visualization)

### Installation

1. Set up the knowledge graph builder:
   ```bash
   cd knowledge_graph_builder
   pip install -r requirements.txt
   ```

2. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

3. Configure environment variables in `knowledge_graph_builder/.env`

### Running the Application

1. Start the backend:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Alternatively, run the Streamlit UI:
   ```bash
   cd knowledge_graph_builder
   streamlit run app.py
   ```

## Features

- Generate comprehensive knowledge graphs on any topic
- Multi-agent architecture for research, synthesis, and mapping
- Interactive visualization with downloadable SVG files
- Modern React frontend with real-time status updates
- RESTful API for programmatic access

## License

MIT