import streamlit as st
import uuid
import requests
from langflow.load import run_flow_from_json
from typing import Optional

# Define your API URL and other constants
BASE_API_URL = "http://your-api-url-here"  # Replace with your actual API URL

# Function to generate unique session_id if it doesn't exist
def get_session_id():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

# Function to run the flow with the correct parameters
def run_flow(message: str,
             session_id: str,
             sender: str,
             sender_name: str,
             tweaks: Optional[dict] = None) -> dict:
    """
    Runs the flow with the given message and session information.

    :param message: The message to send to the flow
    :param session_id: Unique session ID
    :param sender: Sender's identifier (email or name)
    :param sender_name: Name of the sender
    :param tweaks: Any additional tweaks or parameters
    :return: JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/flow_name_here"  # Define your flow URL

    payload = {
        "input_value": message,
        "session_id": session_id,  # Ensure session_id is passed to the relevant fields
        "sender": sender,
        "sender_name": sender_name,
        "tweaks": tweaks or {}
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Will raise an error if the response is not 200 OK
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}

# Tweaks for LangFlow
TWEAKS = {
    "ChatInput-6Lgre": {
        "input_value": "brief some good points about inspection",
        "sender": "User",
        "sender_name": "Archi",
        "session_id": "",  # To be populated
        "should_store_message": True
    },
    "ChatOutput-UJU7A": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "My friend",
        "session_id": "",  # To be populated
        "should_store_message": True
    },
    "Memory-w84zU": {
        "n_messages": 100,
        "order": "Ascending",
        "sender": "Machine and User",
        "sender_name": "",
        "session_id": "",  # To be populated
        "template": "{sender_name}: {text}"
    },
    "Chroma-LAhGk": {
        "retrieval_function": "semantic_search",
        "n_results": 5,
        "session_id": "",  # To be populated
        "input_value": "search query here"
    },
    "TextInput-AeCmf": {
        "input_value": "User input message here",
        "session_id": "",  # To be populated
        "sender": "User",
        "sender_name": "Archi"
    },
    "SplitText-rbRaI": {
        "input_value": "some long text to be split",
        "session_id": "",  # To be populated
        "output_length": 500
    },
    "Chroma-gNlPk": {
        "input_value": "Chroma vector here",
        "session_id": "",  # To be populated
        "n_results": 5
    }
}

# Function to run the chat flow
def chat(prompt: str):
    # Ensure session_id is available
    session_id = get_session_id()
    
    # Sender details
    sender_email = "user_email@example.com"  # Replace with actual sender email or ID
    sender_name = "User Name"  # Replace with actual sender name

    # Add user message to the chat history
    st.session_state.messages.append(("human", prompt))

    # Display user message in the chat
    with st.chat_message("human"):
        st.markdown(prompt)

    # Default value for output to avoid UnboundLocalError
    output = "Sorry, something went wrong, and I couldn't generate an answer."

    # Generate the input string for the AI
    with st.chat_message("ai"):
        history = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.messages])
        query = f"{history}\nAI:"

        # Pass query to the input_value parameter
        inputs = query
        tweaks = {
            "session_id": session_id,  # Pass the unique session ID
            "sender": sender_email,  # Sender info
            "sender_name": sender_name,  # Sender name
            **TWEAKS  # Include the rest of the tweaks
        }

        # Update session_id for the relevant components
        tweaks["ChatInput-6Lgre"]["session_id"] = session_id
        tweaks["ChatOutput-UJU7A"]["session_id"] = session_id
        tweaks["Memory-w84zU"]["session_id"] = session_id
        tweaks["Chroma-LAhGk"]["session_id"] = session_id
        tweaks["TextInput-AeCmf"]["session_id"] = session_id
        tweaks["SplitText-rbRaI"]["session_id"] = session_id
        tweaks["Chroma-gNlPk"]["session_id"] = session_id

        # Run the flow with the updated parameters
        try:
            result = run_flow_from_json(
                flow="./LangRAG.json",  # Define your flow file here
                input_value=inputs,
                tweaks=tweaks  # Pass the updated tweaks with session_id
            )
            
            # Extract and display AI output
            if "ChatOutput-UJU7A" in result:
                output = result["ChatOutput-UJU7A"]["data_template"].format(text=result["ChatOutput-UJU7A"]["input_value"])
            
        except Exception as e:
            st.markdown(f"Error occurred: {str(e)}")

    # Display AI response in the chat
    with st.chat_message("ai"):
        st.markdown(output)

    # Log AI response to chat history
    st.session_state.messages.append(("ai", output))

# Streamlit configuration
st.set_page_config(page_title="AI for AI")
st.title("Chat RAG")

system_prompt = "You're a helpful assistant who can explain concepts."
if "messages" not in st.session_state:
    st.session_state.messages = [("system", system_prompt)]

if "disabled" not in st.session_state:
    st.session_state.disabled = False

with st.chat_message("ai"):
    st.markdown("Hi! I'm your AI assistant.")

# Display chat messages
for role, message in st.session_state.messages:
    if role == "system":
        continue
    with st.chat_message(role):
        st.markdown(message)

current_chat_message = st.container()
prompt = st.chat_input("Ask your question here...", disabled=st.session_state.disabled)

if prompt:
    chat(prompt)
