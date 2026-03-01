import streamlit as st
from langflow.load import run_flow_from_json

# Define your Langflow project settings
FLOW_JSON_PATH = "LLM_Langflow_AI_Agent.json"

st.title("Socratic AI Agent")

if prompt := st.chat_input("Ask a question about your PDF..."):
    # Tweaks mapping using the IDs from your uploaded file
    tweaks = {
      "ChatInput-UJ4St": {
        "input_value": prompt
      },
      "AstraDB-gqqNc": {
        "token": st.secrets["ASTRA_DB_APPLICATION_TOKEN"],
        "api_endpoint": "https://d98a5850-19a2-44c4-9cd9-d9abc9f6f5bb-us-east1.apps.astra.datastax.com",
        "collection_name": "llm_collect"
      },
      "GroqModel-7Tvzb": {
        "groq_api_key": st.secrets["GROQ_API_KEY"]
      },
      "OllamaEmbeddings-PVNW8": {
        "base_url": "https://manjushatambe-ollama-space.hf.space" # Or your HF Space URL
      }
    }

    with st.spinner("Processing..."):
        result = run_flow_from_json(
            flow=FLOW_JSON_PATH,
            input_value=prompt,
            tweaks=tweaks
        )
        # Extract and display the final message
        st.write(result[0].outputs[0].results["message"].text)