import streamlit as st
from langflow.load import load_flow_from_json

# Page configuration
st.set_page_config(page_title="AI Portfolio Assistant", page_icon="🤖")
st.title("💬 My AI Agent")
st.markdown("Explore this AI assistant built with Langflow and Streamlit.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load the Langflow project
FLOW_PATH = "flow.json" # Change to your uploaded filename

# Display chat history from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Langflow
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                flow = load_flow_from_json(FLOW_PATH)
                # Ensure the input matches your flow's input key (default is often 'input_value')
                result = flow({"input_value": prompt})
                response = result.get("result", "I'm sorry, I couldn't process that.")
                st.markdown(response)
                # Save assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")