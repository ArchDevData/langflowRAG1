import os
import streamlit as st
from langflow.load import run_flow_from_json

# Streamlit Page Config
st.set_page_config(page_title="LangFlow Chatbot Deployment", layout="wide")
st.title("🤖 LangFlow Chatbot with File Attachments")

# Define File Paths and TWEAKS
FLOW_FILE = "./LangRAG.json"  # Replace with your actual flow file path
TWEAKS = {
    # Copy your TWEAKS dictionary here
    # (Add your full TWEAKS object here for customization)
}

# Run LangFlow on Button Click
def run_langflow_chat(input_message, tweaks):
    try:
        # Running the flow with user input
        result = run_flow_from_json(
            flow=FLOW_FILE,
            input_value=input_message,
            fallback_to_env_vars=True,
            tweaks=tweaks,
        )
        return result
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Uploading and Attaching Files
st.write("### File Upload for Context")
uploaded_files = st.file_uploader(
    "Upload multiple files to include in context (e.g., PDFs, DOCX)", accept_multiple_files=True
)

if uploaded_files:
    temp_dir = "uploaded_files"
    os.makedirs(temp_dir, exist_ok=True)
    file_paths = []

    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_paths.append(file_path)
        st.write(f"Uploaded: {uploaded_file.name}")

    # Update TWEAKS dynamically for new file paths
    for i, file_path in enumerate(file_paths):
        TWEAKS[f"File-{i}"] = {"path": file_path, "silent_errors": False}

# Chat Interface
st.write("### Chat with LangFlow Bot")
user_input = st.text_input("Enter your query:")

if st.button("Submit"):
    if user_input:
        response = run_langflow_chat(user_input, TWEAKS)
        if response:
            st.write("### Response:")
            st.write(response)
    else:
        st.warning("Please enter a query before submitting.")

