import os
import uuid
import copy
import traceback
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

# Check if the flow file exists
if not os.path.exists("./LangRAG.json"):
    st.error("Error: Flow file 'LangRAG.json' not found. Please ensure it is in the correct directory.")
else:
    # Streamlit UI
    st.title("Langflow Chatbot")
    st.write("Welcome! Ask me anything, and I'll fetch answers based on the documents and context.")

    # Generate a unique session ID for tracking
    session_id = str(uuid.uuid4())

    # Capture user input
    user_input = st.text_input("You:", "")

    # Validate input
    if user_input.strip() == "":
        st.warning("Please enter a valid input.")
    elif st.button("Submit"):
        with st.spinner("Processing your input..."):
            try:
                # Use a copy of TWEAKS for each request
                tweaks_copy = copy.deepcopy(TWEAKS)
                tweaks_copy["ChatInput-6Lgre"]["input_value"] = user_input
                tweaks_copy["ChatInput-6Lgre"]["session_id"] = session_id
                tweaks_copy["ChatOutput-UJU7A"]["session_id"] = session_id

                # Run the Langflow flow
                result = run_flow_from_json(flow="./LangRAG.json", input_value=user_input, tweaks=tweaks_copy)

                # Debugging: Display the result object (optional)
                st.write("Debugging Result:", result)

                # Check result structure and display output
                if "ChatOutput-UJU7A" in result and "input_value" in result["ChatOutput-UJU7A"]:
                    response = result["ChatOutput-UJU7A"]["data_template"].format(
                        text=result["ChatOutput-UJU7A"]["input_value"]
                    )
                    st.write(f"Assistant: {response}")
                else:
                    st.write("Assistant: Sorry, I couldn't generate an answer.")
            except Exception as e:
                st.error("An error occurred while processing your request.")
                st.text(traceback.format_exc())

    # Validate Azure API keys and endpoints
    if not TWEAKS["AzureOpenAIEmbeddings-GS6Lh"]["api_key"] or not TWEAKS["AzureOpenAIModel-qhSVT"]["api_key"]:
        st.error("Azure API keys are missing or invalid. Please update the TWEAKS dictionary.")
