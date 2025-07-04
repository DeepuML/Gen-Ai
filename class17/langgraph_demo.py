# # langgraph_agent.py
# from langgraph.graph import StateGraph, END
# from typing_extensions import TypedDict
# from euri_llm import euri_completion


# # ✅ Step 1: Define a state schema using TypedDict
# class GraphState(TypedDict):
#     input: str
#     research: str
#     summary: str

# # ✅ Step 2: Define node functions
# def researcher(state: GraphState) -> dict:
#     question = state["input"]
#     response = euri_completion([{"role": "user", "content": f"Research: {question}"}])
#     return {"research": response}

# def summarizer(state: GraphState) -> dict:
#     research = state["research"]
#     summary = euri_completion([{"role": "user", "content": f"Summarize this: {research}"}])
#     return {"summary": summary}

# # ✅ Step 3: Define and compile LangGraph
# graph = StateGraph(GraphState)  # schema required here!
# graph.add_node("researcher", researcher)
# graph.add_node("summarizer", summarizer)
# graph.set_entry_point("researcher")
# graph.add_edge("researcher", "summarizer")
# graph.set_finish_point("summarizer")

# compiled_graph = graph.compile()

# # ✅ Step 4: Run the graph
# result = compiled_graph.invoke({"input": "Impact of AI in healthcare"})
# print("\n✅ Final Summary:\n", result["summary"])


# langgraph_agent.py

from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import Optional
from euri_llm import euri_completion  # <- Make sure this function is defined properly


# ✅ Step 1: Define state using Pydantic BaseModel
class GraphState(BaseModel):
    input: str
    research: Optional[str] = None
    summary: Optional[str] = None


# ✅ Step 2: Define node functions
def researcher(state: GraphState) -> dict:
    question = state.input
    response = euri_completion([{"role": "user", "content": f"Research: {question}"}])
    return {"research": response}

def summarizer(state: GraphState) -> dict:
    research_text = state.research
    summary = euri_completion([{"role": "user", "content": f"Summarize this: {research_text}"}])
    return {"summary": summary}


# ✅ Step 3: Build and compile LangGraph
graph = StateGraph(GraphState)
graph.add_node("researcher", researcher)
graph.add_node("summarizer", summarizer)
graph.set_entry_point("researcher")
graph.add_edge("researcher", "summarizer")
graph.set_finish_point("summarizer")

compiled_graph = graph.compile()

# ✅ Step 4: Run the graph
result = compiled_graph.invoke({"input": "Impact of AI in healthcare"})
print("\n✅ Final Summary:\n", result["summary"])
