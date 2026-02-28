import streamlit as st
import os
from langflow.load import run_flow_from_json

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Workflow App",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Workflow App")
st.caption("Powered by Langflow + OpenAI")

# -----------------------------
# LOAD API KEY (Streamlit Cloud Compatible)
# -----------------------------
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# -----------------------------
# SESSION STATE FOR CHAT
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------
prompt = st.chat_input("Type your message here...")

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Run Langflow
    with st.spinner("Thinking..."):
        try:
            result = run_flow_from_json(
                flow="flow.json",   # Your uploaded file
                input_value=prompt
            )

            # Some flows return dicts
            if isinstance(result, dict):
                output = result.get("output", str(result))
            else:
                output = str(result)

        except Exception as e:
            output = f"Error: {str(e)}"

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(output)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": output})