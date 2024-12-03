import streamlit as st
from langflow.load import run_flow_from_json
import sys
import pysqlite3 as sqlite3
import uuid
import os  # For file and path handling

sys.modules["sqlite3"] = sqlite3

# Define Langflow tweaks
TWEAKS = {
    "ChatInput-6Lgre": {
        "files": "",
        "input_value": "",
        "sender": "User",
        "sender_name": "Archi",
        "session_id": "",
        "should_store_message": True,
    },
    "ChatOutput-UJU7A": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "My friend",
        "session_id": "",
        "should_store_message": True,
    },
    "File-7ysYy": {
        "path": "",
        "silent_errors": False,
        "session_id": "",
    },
}

# Streamlit Frontend
st.title("Langflow Chatbot with Session Management")
st.write("Welcome! Upload a file to add context, then ask your question.")

# Initialize session management
if "session_data" not in st.session_state:
    st.session_state.session_data = {
        "session_id": str(uuid.uuid4()),  # Generate unique session ID
        "file_path": "",
    }

# Set session_id for components
session_id = st.session_state.session_data["session_id"]

# File uploader
uploaded_file = st.file_uploader(
    "Upload a file to include in the chatbot context:", type=["txt", "pdf", "docx"]
)

if uploaded_file:
    # Save uploaded file
    temp_dir = "./tmp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Update session state and TWEAKS
    st.session_state.session_data["file_path"] = temp_file_path
    TWEAKS["File-7ysYy"]["path"] = temp_file_path
    TWEAKS["File-7ysYy"]["session_id"] = session_id
    st.success(f"File '{uploaded_file.name}' uploaded and linked successfully.")

# Capture user input
user_input = st.text_input("You:", "")

if user_input:
    # Update TWEAKS with user input and session ID
    TWEAKS["ChatInput-6Lgre"]["input_value"] = user_input
    TWEAKS["ChatInput-6Lgre"]["session_id"] = session_id
    TWEAKS["ChatOutput-UJU7A"]["session_id"] = session_id

    # Debugging output
    st.write("Debugging TWEAKS:", TWEAKS)

    # Ensure file is linked
    if not st.session_state.session_data["file_path"]:
        st.warning("Please upload a file before asking a question.")
    else:
        try:
            # Execute Langflow logic
            result = run_flow_from_json(
                flow="./LangRAG.json", input_value=user_input, tweaks=TWEAKS
            )

            # Process the assistant's response
            if "ChatOutput-UJU7A" in result:
                response_text = result["ChatOutput-UJU7A"]["data_template"].format(
                    text=result["ChatOutput-UJU7A"]["input_value"]
                )
                st.write(f"Assistant: {response_text}")
            else:
                st.write("Assistant: Sorry, I couldn't generate an answer.")
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
