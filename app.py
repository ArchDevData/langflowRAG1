import streamlit as st
from langflow.load import run_flow_from_json
import sys
import pysqlite3 as sqlite3
import uuid
import os  # For file and path handling

sys.modules["sqlite3"] = sqlite3

# Define Langflow tweaks
TWEAKS = {
    "ChatInput-6Lgre": {},
    "ChatOutput-UJU7A": {},
    "TextInput-AeCmf": {},
    "Chroma-LAhGk": {},
    "SplitText-rbRaI": {},
    "Memory-w84zU": {},
    "Chroma-gNlPk": {},
    "ParseData-oI1Nx": {},
    "Prompt-s8d9d": {},
    "TextOutput-BY5DW": {},
    "AzureOpenAIEmbeddings-GS6Lh": {},
    "AzureOpenAIModel-qhSVT": {},
    "File-7ysYy": {}
}

# Streamlit Frontend
st.title("Langflow Chatbot with Chat History and File Upload")
st.write("Welcome! Upload a file to add context, then ask your question.")

# Initialize session states
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []  # Store chat history (user and assistant messages)

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

# Display chat history
st.markdown("### Chat History")
for role, message in st.session_state.messages:
    if role == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Assistant:** {message}")

# Input box for user query
user_input = st.text_input("You:", "")

# Process user input
if user_input:
    # Update TWEAKS with user input and session ID
    TWEAKS["ChatInput-6Lgre"]["input_value"] = user_input
    TWEAKS["ChatInput-6Lgre"]["session_id"] = st.session_state.session_id
    TWEAKS["ChatOutput-UJU7A"]["session_id"] = st.session_state.session_id
    TWEAKS["File-7ysYy"]["session_id"] = st.session_state.session_id

    # Add user message to chat history
    st.session_state.messages.append(("user", user_input))

    # Ensure a file is linked before processing
    if not TWEAKS["File-7ysYy"]["path"]:
        st.warning("Please upload a file before asking a question.")
    else:
        try:
            # Run the Langflow flow
            result = run_flow_from_json(
                flow="./LangRAG.json", input_value=user_input, tweaks=TWEAKS
            )
            
            # Extract the assistant's response
            if "ChatOutput-UJU7A" in result:
                response = result["ChatOutput-UJU7A"]["data_template"].format(
                    text=result["ChatOutput-UJU7A"]["input_value"]
                )
                st.session_state.messages.append(("assistant", response))
                st.write(f"**Assistant:** {response}")
            else:
                response = "Sorry, I couldn't generate an answer."
                st.session_state.messages.append(("assistant", response))
                st.write(f"**Assistant:** {response}")
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
