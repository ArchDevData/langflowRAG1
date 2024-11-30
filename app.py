import streamlit as st
from langflow.load import run_flow_from_json

# Define your Langflow tweaks (as provided)
TWEAKS = {
    "ChatInput-6Lgre": {
        "files": "",
        "input_value": "",  # Default empty, will update with user input
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
        "persist_directory": "D:/OneDrive - Larsen & Toubro/All_Work/GenAI/RAG_Langflow/Chromadb",
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
        "persist_directory": "D:/OneDrive - Larsen & Toubro/All_Work/GenAI/RAG_Langflow/Chromadb",
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
        "path": "APPENDIX 4_S040718-19-22.docx",
        "silent_errors": False
    },
    "File-uOTiK": {
        "path": "Customer Preference.docx",
        "silent_errors": False
    },
    "File-rucyj": {
        "path": "Agency_Approved.docx",
        "silent_errors": False
    },
    "File-fjFUf": {
        "path": "APPENDIX 4_S040718-19-22.pdf",
        "silent_errors": False
    },
    "File-DrLLw": {
        "path": "EA-MZ-FA0000-CCV-P14-00003-00_S040718-19-22.pdf",
        "silent_errors": False
    },
    "File-loN7R": {
        "path": "EA-MZ-FA0000-CCV-P14-00003-00_S040718-19-22.pdf",
        "silent_errors": False
    }
}

# Set up Streamlit frontend
st.title("Langflow Chatbot")
st.write("Welcome! Ask me anything, and I'll fetch answers based on the documents and context.")

# Capture user input
user_input = st.text_input("You:", "")

# Check if user has provided input
if user_input:
    # Update TWEAKS with user input
    TWEAKS["ChatInput-6Lgre"]["input_value"] = user_input
    
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

