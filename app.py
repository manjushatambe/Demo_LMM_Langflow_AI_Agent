import streamlit as st
import asyncio
from langflow.graph import Graph

st.set_page_config(page_title="AI App", page_icon="🤖")
st.title("🤖 AI Workflow App")

# Load flow
@st.cache_resource
def load_graph():
    return Graph.from_json("flow.json")

graph = load_graph()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask something...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        try:
            result = asyncio.run(
                graph.arun(
                    inputs={"ChatInput-ZPFS5": prompt}
                )
            )

            # Extract final output
            output = list(result.values())[-1]

        except Exception as e:
            output = f"Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(str(output))

    st.session_state.messages.append({"role": "assistant", "content": str(output)})