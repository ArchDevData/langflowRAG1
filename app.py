import streamlit as st  
from langflow.load import run_flow_from_json  
import sys  
import pysqlite3 as sqlite3  
import uuid  
import os  # For file and path handling  
  
# Ensure sqlite3 is properly handled  
sys.modules["sqlite3"] = sqlite3  
  
# Define Langflow tweaks  
TWEAKS = {  
    "ChatInput-6Lgre": {  
        "files": "",  
        "input_value": "",  
        "sender": "User",  
        "sender_name": "Archi",  
        "session_id": "",  # Will be set below  
        "should_store_message": True  
    },  
    "ChatOutput-UJU7A": {  
        "data_template": "{text}",  
        "input_value": "",  
        "sender": "Machine",  
        "sender_name": "My friend",  
        "session_id": "",  # Will be set below  
        "should_store_message": True  
    },  
    "File-7ysYy": {  
        "path": "",  
        "silent_errors": False,  
        "session_id": ""  # Will be set below  
    }  
}  
  
# Streamlit Frontend  
st.title("Langflow Chatbot with File Upload")  
st.write("Welcome! Upload a file to add context, then ask your question.")  
  
# Initialize session ID  
if "session_id" not in st.session_state:  
    st.session_state.session_id = str(uuid.uuid4())  
  
# File uploader  
uploaded_file = st.file_uploader("Upload a file to include in the chatbot context:", type=["txt", "pdf", "docx"])  
if uploaded_file:  
    # Create a temporary directory for storing files  
    temp_dir = "./tmp"  
    os.makedirs(temp_dir, exist_ok=True)  
  
    # Save the uploaded file  
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)  
    with open(temp_file_path, "wb") as f:  
        f.write(uploaded_file.getbuffer())  
  
    # Update the file path and session ID in TWEAKS  
    TWEAKS["File-7ysYy"]["path"] = temp_file_path  
    TWEAKS["File-7ysYy"]["session_id"] = st.session_state.session_id  
    st.success(f"File '{uploaded_file.name}' uploaded and linked successfully.")  
  
# Capture user input  
user_input = st.text_input("You:", "")  
  
# Check if user input is provided  
if user_input:  
    # Update TWEAKS with user input and session ID  
    TWEAKS["ChatInput-6Lgre"]["input_value"] = user_input  
    TWEAKS["ChatInput-6Lgre"]["session_id"] = st.session_state.session_id  
    TWEAKS["ChatOutput-UJU7A"]["session_id"] = st.session_state.session_id  
    TWEAKS["File-7ysYy"]["session_id"] = st.session_state.session_id  # Ensure session_id is set for File  
  
    # Debugging output  
    st.write("Debugging TWEAKS:", TWEAKS)  
  
    # Ensure a file is linked  
    if not TWEAKS["File-7ysYy"]["path"]:  
        st.warning("Please upload a file before asking a question.")  
    else:  
        try:  
            # Run the Langflow process  
            result = run_flow_from_json(  
                flow="./LangRAG.json", input_value=user_input, tweaks=TWEAKS  
            )  
            if "ChatOutput-UJU7A" in result:  
                # Display the assistant's response  
                assistant_response = result["ChatOutput-UJU7A"]["input_value"]  
                st.write(f"Assistant: {assistant_response}")  
            else:  
                st.error("No response from the assistant.")  
        except Exception as e:  
            st.error(f"An error occurred: {str(e)}")  
