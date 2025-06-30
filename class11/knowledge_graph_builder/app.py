# Install the required package (run this in terminal, not in the script):
# pip install python-multipart

from workflows.langgraph_router import autonomous_pipeline
from utils.graphviz_exporter import export_to_svg
import os
import base64
import json

# Ensure outputs directory exists
os.makedirs("data/outputs", exist_ok=True)

# Configuration flag (set to False by default to use YouTube API)
use_serpapi_youtube = False

# Function to generate knowledge graph
def generate_knowledge_graph(topic, use_serpapi_youtube=False):
    try:
        # Run the autonomous pipeline
        result = autonomous_pipeline({"input": topic, "use_serpapi_youtube": use_serpapi_youtube})
        graph = result.get("result", {})
        raw_data = result.get("raw_info", {})
        
        # Export the graph to SVG
        svg_path = export_to_svg(graph, file_name=f"{topic.replace(' ', '_').lower()[:30]}")
        
        return {
            "success": True,
            "graph": graph,
            "raw_data": raw_data,
            "svg_path": svg_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Function to extract concepts and categorize them
def extract_concepts_from_graph(graph):
    concepts = set()
    relationships = []
    
    for node in graph.get("nodes", []):
        node_id = node.get("id", "")
        if node_id and "Learning Path" not in node_id:
            concepts.add(node_id)
    
    for edge in graph.get("edges", []):
        source = edge.get("source", "")
        target = edge.get("target", "")
        if source and target:
            if "Learning Path" in source or "Learning Path" in target:
                relationships.append((source, target))
    
    beginner_concepts = []
    intermediate_concepts = []
    advanced_concepts = []

    for concept in concepts:
        cl = concept.lower()
        if "introduction" in cl or "basics" in cl or "fundamental" in cl:
            beginner_concepts.append(concept)
        elif "advanced" in cl or "deep" in cl or "expert" in cl:
            advanced_concepts.append(concept)
        else:
            intermediate_concepts.append(concept)
    
    return {
        "beginner": beginner_concepts,
        "intermediate": intermediate_concepts,
        "advanced": advanced_concepts,
        "relationships": relationships
    }

# Script entry point
if __name__ == "__main__":
    topic = "Machine Learning Basics"
    result = generate_knowledge_graph(topic)
    
    if result["success"]:
        print(f"✅ Knowledge graph for '{topic}' created successfully!")
        print(f"SVG saved to: {result['svg_path']}")
        
        concepts = extract_concepts_from_graph(result["graph"])
        
        print("\n🟢 Beginner concepts:")
        for c in concepts["beginner"]:
            print(f"- {c}")
        
        print("\n🟡 Intermediate concepts:")
        for c in concepts["intermediate"]:
            print(f"- {c}")
        
        print("\n🔴 Advanced concepts:")
        for c in concepts["advanced"]:
            print(f"- {c}")
    else:
        print(f"❌ Error generating graph: {result['error']}")
