import streamlit as st
from langflow.load import run_flow_from_json
import sys
import pysqlite3 as sqlite3
import uuid
import os  # For file and path handling

sys.modules["sqlite3"] = sqlite3

# Define LangFlow tweaks
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

# Initialize session state
def initialize_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Store chat history (user and assistant messages)
    if "file_path" not in st.session_state:
        st.session_state.file_path = None


# Save uploaded file and return its path
def save_uploaded_file(uploaded_file):
    temp_dir = "./tmp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_file_path


# Display chat history
def display_chat_history():
    st.markdown("### Chat History")
    for role, message in st.session_state.messages:
        if role == "user":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**Assistant:** {message}")


# Process user input with LangFlow
def process_user_input(user_input):
    # Update TWEAKS with user input and session information
    TWEAKS["ChatInput-6Lgre"]["input_value"] = user_input
    TWEAKS["ChatInput-6Lgre"]["session_id"] = st.session_state.session_id
    TWEAKS["ChatOutput-UJU7A"]["session_id"] = st.session_state.session_id
    TWEAKS["File-7ysYy"]["session_id"] = st.session_state.session_id

    # Ensure a file is linked before processing
    if not st.session_state.file_path:
        st.warning("Please upload a file before asking a question.")
        return

    TWEAKS["File-7ysYy"]["path"] = st.session_state.file_path

    try:
        # Run LangFlow process
        result = run_flow_from_json(
            flow="./LangRAG.json", input_value=user_input, tweaks=TWEAKS
        )

        # Extract and display the assistant's response
        if "ChatOutput-UJU7A" in result:
            response = result["ChatOutput-UJU7A"]["data_template"].format(
                text=result["ChatOutput-UJU7A"]["input_value"]
            )
        else:
            response = "Sorry, I couldn't generate an answer."

        # Add assistant's response to chat history
        st.session_state.messages.append(("assistant", response))
        st.write(f"**Assistant:** {response}")

    except Exception as e:
        st.error(f"Error occurred: {str(e)}")


# Main Streamlit app
initialize_session()

st.title("LangFlow Chatbot with Chat History and File Upload")
st.write("Welcome! Upload a file to add context, then ask your question.")

# File upload section
uploaded_file = st.file_uploader(
    "Upload a file to include in the chatbot context:", type=["txt", "pdf", "docx"]
)

if uploaded_file:
    st.session_state.file_path = save_uploaded_file(uploaded_file)
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

# Display chat history
display_chat_history()

# Input box for user queries
user_input = st.text_input("You:", "")

if user_input:
    # Add user input to chat history
    st.session_state.messages.append(("user", user_input))
    # Process the user input
    process_user_input(user_input)

# Cleanup logic (optional): Delete temporary files
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.write("Chat history cleared.")

if st.button("Delete Uploaded File"):
    if st.session_state.file_path:
        os.remove(st.session_state.file_path)
        st.session_state.file_path = None
        st.write("Uploaded file deleted.")
    else:
        st.warning("No file to delete.")
