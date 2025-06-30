# LangGraph decision router logic
from langgraph.graph import StateGraph
from typing import TypedDict

# Fix imports to use absolute imports
from knowledge_graph_builder.agents.researcher import run_researcher
from knowledge_graph_builder.agents.synthesizer import run_synthesizer
from knowledge_graph_builder.agents.mapper import run_mapper

class GraphState(TypedDict):
    input: str
    use_serpapi_youtube: bool
    raw_info: dict
    summary: str
    result: dict

def build_langgraph():
    graph = StateGraph(GraphState)

    def wrapped_researcher(state: GraphState):
        return {"raw_info": run_researcher(state["input"], state.get("use_serpapi_youtube", False))}

    def wrapped_synthesizer(state: GraphState):
        return {"summary": run_synthesizer(state["raw_info"])}

    def wrapped_mapper(state: GraphState):
        return {"result": run_mapper(state["summary"])}

    graph.add_node("research", wrapped_researcher)
    graph.add_node("synthesize", wrapped_synthesizer)
    graph.add_node("map", wrapped_mapper)

    graph.set_entry_point("research")
    graph.add_edge("research", "synthesize")
    graph.add_edge("synthesize", "map")

    return graph.compile()

def autonomous_pipeline(input_data):
    langgraph_flow = build_langgraph()
    
    # Handle both string input and dictionary input
    if isinstance(input_data, str):
        # For backward compatibility
        topic = input_data
        use_serpapi_youtube = False
    else:
        # New format with options
        topic = input_data["input"]
        use_serpapi_youtube = input_data.get("use_serpapi_youtube", False)
    
    # Invoke the graph with all parameters
    result = langgraph_flow.invoke({
        "input": topic,
        "use_serpapi_youtube": use_serpapi_youtube
    })
    
    # Return both the graph result and the raw research data
    return {
        "result": result["result"],
        "raw_info": result.get("raw_info", {})
    }
# Example usage
if __name__ == "__main__":
    topic = "Artificial Intelligence"
    result = autonomous_pipeline(topic)
    print("Knowledge Graph Result:", result)