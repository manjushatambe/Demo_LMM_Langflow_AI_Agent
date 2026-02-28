import streamlit as st
import requests

st.set_page_config(page_title="AI App", page_icon="🤖")
st.title("🤖 AI Workflow App")

FLOW_ID = "cd60990e-1e23-4a7f-8de4-b18fbf6a3f38"
LANGFLOW_URL = "https://manjushatambe-llm-langflow-ai-agent-demo.hf.space"

API_URL = f"{LANGFLOW_URL}/api/v1/run/{FLOW_ID}"

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
            response = requests.post(
                f"{LANGFLOW_URL}/api/v1/run/{FLOW_ID}",
                json={
                    "input_value": prompt,
                    "output_type": "chat",
                    "input_type": "chat"
                }
            )

            data = response.json()
            output = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]

        except Exception as e:
            output = f"Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(output)

    st.session_state.messages.append({"role": "assistant", "content": output})