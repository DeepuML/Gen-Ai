from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sys
import os
import uuid
import json
from datetime import datetime

# Add knowledge_graph_builder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the autonomous pipeline
from knowledge_graph_builder.workflows.langgraph_router import autonomous_pipeline
from knowledge_graph_builder.utils.graphviz_exporter import export_to_svg

app = FastAPI(title="Knowledge Graph API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure output directory exists
os.makedirs("../knowledge_graph_builder/data/outputs", exist_ok=True)
os.makedirs("../knowledge_graph_builder/database", exist_ok=True)

# Store job status
jobs = {}

class QueryInput(BaseModel):
    query: str

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str

# Background task to generate graph
def generate_graph_task(job_id: str, query: str):
    try:
        # Update job status
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["steps"].append("Starting research...")
        
        # Run the pipeline
        graph_data = autonomous_pipeline(query)
        jobs[job_id]["steps"].append("Research complete")
        jobs[job_id]["steps"].append("Synthesizing information...")
        
        # Generate SVG
        file_name = f"{query.replace(' ', '_').lower()[:30]}_{job_id[:8]}"
        svg_path = export_to_svg(graph_data, file_name=file_name, output_dir="../knowledge_graph_builder/database")
        jobs[job_id]["steps"].append("Knowledge graph generated")
        
        # Update job with result
        jobs[job_id]["status"] = "completed"
        # Save user query and graph data to a JSON file
        output_data = {
            "query": query,
            "graph_data": graph_data
        }
        json_output_path = os.path.join("../knowledge_graph_builder/database", f"user_data_{job_id}.json")
        with open(json_output_path, "w") as f:
            json.dump(output_data, f, indent=4)

        jobs[job_id]["result"] = {
            "svg_path": svg_path,
            "graph_data": graph_data,
            "json_output_path": json_output_path
        }
    except Exception as e:
        # Handle errors
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.post("/run", response_model=JobResponse)
def run_pipeline(input: QueryInput, background_tasks: BackgroundTasks):
    # Create a unique job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job
    jobs[job_id] = {
        "query": input.query,
        "status": "queued",
        "created_at": datetime.now().isoformat(),
        "steps": ["Job queued"],
        "result": None,
        "error": None
    }
    
    # Start background task
    background_tasks.add_task(generate_graph_task, job_id, input.query)
    
    return JobResponse(
        job_id=job_id,
        status="queued",
        message="Knowledge graph generation started"
    )

@app.get("/status/{job_id}")
def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job["status"],
        "steps": job["steps"],
        "error": job["error"] if job["status"] == "failed" else None
    }

@app.get("/result/{job_id}")
def get_job_result(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail=f"Job is not completed. Current status: {job['status']}")
    
    return job["result"]

@app.get("/download/{job_id}")
def download_svg(job_id: str):
    if job_id not in jobs or jobs[job_id]["status"] != "completed":
        raise HTTPException(status_code=404, detail="Result not found or job not completed")
    
    svg_path = jobs[job_id]["result"]["svg_path"]
    return FileResponse(svg_path, media_type="image/svg+xml", filename=os.path.basename(svg_path))