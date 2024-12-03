import streamlit as st
from langflow.load import run_flow_from_json
import sys
import pysqlite3 as sqlite3
import uuid  # To generate a unique session ID

sys.modules["sqlite3"] = sqlite3

# Define your Langflow tweaks (as provided)
TWEAKS = {
    "ChatInput-6Lgre": {
        "files": "",
        "input_value": "",  # Default empty, will update with user input
        "sender": "User",
        "sender_name": "Archi",
        "session_id": "",  # To be set dynamically
        "should_store_message": True
    },
    "ChatOutput-UJU7A": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "My friend",
        "session_id": "",  # To be set dynamically
        "should_store_message": True
    },
    "File-7ysYy": {
        "path": "",  # To be dynamically set
        "silent_errors": False
    }
}

# Set up Streamlit frontend
st.title("Langflow Chatbot")
st.write("Welcome! Ask me anything, and I'll fetch answers based on the documents and context.")

# File uploader
uploaded_file = st.file_uploader("Upload a file to include in the chatbot context:", type=["txt", "pdf", "docx"])

if uploaded_file:
    # Save the uploaded file to a temporary directory
    temp_file_path = f"./tmp/{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Update the file path in TWEAKS
    TWEAKS["File-7ysYy"]["path"] = temp_file_path
    st.success(f"File '{uploaded_file.name}' uploaded and linked successfully.")

# Capture user input
user_input = st.text_input("You:", "")

# Initialize session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # Generate unique session ID

# Check if user has provided input
if user_input:
    # Update TWEAKS with user input and session ID
    TWEAKS["ChatInput-6Lgre"]["input_value"] = user_input
    TWEAKS["ChatInput-6Lgre"]["session_id"] = st.session_state.session_id
    TWEAKS["ChatOutput-UJU7A"]["session_id"] = st.session_state.session_id

    # Execute Langflow logic to get response based on the input and tweaks
    try:
        result = run_flow_from_json(flow="./LangRAG.json",
                                    input_value=user_input,
                                    tweaks=TWEAKS)

        # Display the machine's response
        if "ChatOutput-UJU7A" in result:
            st.write(f"Assistant: {result['ChatOutput-UJU7A']['data_template'].format(text=result['ChatOutput-UJU7A']['input_value'])}")
        else:
            st.write("Assistant: Sorry, I couldn't generate an answer.")
    except Exception as e:
        st.write(f"Error: {str(e)}")
