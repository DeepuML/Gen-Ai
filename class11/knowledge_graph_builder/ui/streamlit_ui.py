# knowledge_graph_builder/ui/streamlit_ui.py

import streamlit as st
from agents.researcher import Researcher
from workflows.langgraph_router import LangGraphRouter

st.set_page_config(page_title="Knowledge Graph Builder", layout="wide")

st.title("🔗 Knowledge Graph Builder")
st.markdown("Build a Knowledge Graph using LLM-powered agents.")

query = st.text_input("🔍 Enter your research topic:", "")

if query:
    with st.spinner("Running Researcher Agent..."):
        # Placeholder logic (replace with actual agent call)
        researcher = Researcher()
        # result = researcher.run(query)
        result = f"Research results for **{query}** will be shown here."

        st.success("✅ Research Complete!")
        st.markdown(result)

        st.markdown("---")
        st.button("📤 Export to Graph", on_click=lambda: st.toast("Feature coming soon!"))
