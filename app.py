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
        "should_store_message": True
    },
    "ChatOutput-UJU7A": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "My friend",
        "session_id": "",
        "should_store_message": True
    },
    "TextInput-AeCmf": {
        "input_value": "Test model"
    },
    "Chroma-LAhGk": {
        "allow_duplicates": False,
        "chroma_server_cors_allow_origins": "",
        "chroma_server_grpc_port": None,
        "chroma_server_host": "",
        "chroma_server_http_port": None,
        "chroma_server_ssl_enabled": False,
        "collection_name": "HEIC_Docs",
        "limit": None,
        "number_of_results": 5,
        "persist_directory": "./tmp/Chromadb",
        "search_query": "",
        "search_type": "Similarity"
    },
    "SplitText-rbRaI": {
        "chunk_overlap": 200,
        "chunk_size": 1000,
        "separator": "\n"
    },
    "Memory-w84zU": {
        "n_messages": 100,
        "order": "Ascending",
        "sender": "Machine and User",
        "sender_name": "",
        "session_id": "",
        "template": "{sender_name}: {text}"
    },
    "Chroma-gNlPk": {
        "allow_duplicates": False,
        "chroma_server_cors_allow_origins": "",
        "chroma_server_grpc_port": None,
        "chroma_server_host": "",
        "chroma_server_http_port": None,
        "chroma_server_ssl_enabled": False,
        "collection_name": "HEIC_Docs",
        "limit": None,
        "number_of_results": 5,
        "persist_directory": "./tmp/Chromadb",
        "search_query": "",
        "search_type": "Similarity"
    },
    "ParseData-oI1Nx": {
        "sep": "\n",
        "template": "{text}"
    },
    "Prompt-s8d9d": {
        "template": "Answer user's questions based on the context and history below:\n\n---\n\n{Context}\n\n---\nChat history:\n{History}\n\nQuestion:\n{Question}\n\nAnswer:",
        "History": "",
        "Question": "",
        "Context": ""
    },
    "TextOutput-BY5DW": {
        "input_value": ""
    },
    "AzureOpenAIEmbeddings-GS6Lh": {
        "api_key": "33d36b4d510a4d1583bad02e4a0c2de2",
        "api_version": "2023-05-15",
        "azure_deployment": "text-embedding-ada-002",
        "azure_endpoint": "https://azopenai-use-datasrv-dev-openai-001.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15",
        "dimensions": None
    },
    "AzureOpenAIModel-qhSVT": {
        "api_key": "33d36b4d510a4d1583bad02e4a0c2de2",
        "api_version": "2023-03-15-preview",
        "azure_deployment": "gpt-4o--",
        "azure_endpoint": "https://azopenai-use-datasrv-dev-openai-001.openai.azure.com/openai/deployments/gpt-4o--/chat/completions?api-version=2023-03-15-preview",
        "input_value": "",
        "max_tokens": None,
        "stream": False,
        "system_message": "",
        "temperature": 0.7
    },
    "File-7ysYy": {
        "path": "",
        "silent_errors": False,
        "session_id": ""
    }
}

# Streamlit Frontend
st.title("Langflow Chatbot with File Upload")
st.write("Welcome! Upload a file to add context, then ask your question.")

# Initialize session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# File uploader
uploaded_file = st.file_uploader(
    "Upload a file to include in the chatbot context:", type=["txt", "pdf", "docx"]
)

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
            result = run_flow_from_json(
                flow="./LangRAG.json", input_value=user_input, tweaks=TWEAKS
            )
            if "ChatOutput-UJU7A" in result:
                st.write(
                    f"Assistant: {result['ChatOutput-UJU7A']['data_template'].format(text=result['ChatOutput-UJU7A']['input_value'])}"
                )
            else:
                st.write("Assistant: Sorry, I couldn't generate an answer.")
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
