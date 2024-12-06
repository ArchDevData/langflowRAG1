import streamlit as st
from langflow.load import run_flow_from_json
from typing import Optional
import uuid  # To generate a unique session_id

# Tweaks for LangFlow
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

BASE_API_URL = "http://your-api-url-here"  # Define your base API URL

def run_flow(message: str,
             endpoint: str,
             session_id: str,
             sender: str,
             sender_name: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param session_id: A unique session ID to track the conversation
    :param sender: The sender of the message (e.g., email or identifier)
    :param sender_name: The sender's name
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
        "session_id": session_id,
        "sender": sender,
        "sender_name": sender_name
    }
    
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    else:
        headers = {}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}

def chat(prompt: str):
    with current_chat_message:
        # Block input to prevent sending messages while AI is responding
        st.session_state.disabled = True

        # Generate unique session_id if not already in session state
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        sender_email = "user_email@example.com"  # Replace with actual sender email or ID
        sender_name = "User Name"  # Replace with actual sender name

        # Add user message to chat history
        st.session_state.messages.append(("human", prompt))

        # Display user message in chat message container
        with st.chat_message("human"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("ai"):
            # Get complete chat history, including the latest question as the last message
            history = "\n".join([f"{role}: {msg}" for role, msg in st.session_state.messages])
            query = f"{history}\nAI:"

            # Pass the query as a string (not a dictionary)
            inputs = query  # Directly pass the query as the input_value

            # Call the LangFlow API with session_id, sender, and sender_name
            try:
                result = run_flow_from_json(
                    flow="./LangRAG.json", 
                    input_value=inputs, 
                    tweaks=TWEAKS,
                    session_id=st.session_state.session_id,
                    sender=sender_email,  # Add the sender info
                    sender_name=sender_name  # Add the sender name
                )
                
                # Check if the response contains the desired output
                if "ChatOutput-UJU7A" in result:
                    output = result["ChatOutput-UJU7A"]["data_template"].format(text=result["ChatOutput-UJU7A"]["input_value"])
                else:
                    output = "Sorry, I couldn't generate an answer."
                
                # Display the output
                st.markdown(output)
            except Exception as e:
                output = f"Error occurred: {str(e)}"
                st.markdown(output)

        # Log AI response to chat history
        st.session_state.messages.append(("ai", output))

        # Unblock chat input
        st.session_state.disabled = False
        st.rerun()

# Streamlit configuration
st.set_page_config(page_title="AI for AI")
st.title("Chat RAG")

system_prompt = "You're a helpful assistant who can explain concepts."
if "messages" not in st.session_state:
    st.session_state.messages = [("system", system_prompt)]
if "disabled" not in st.session_state:
    # `disable` flag to prevent user from sending messages while AI is responding
    st.session_state.disabled = False

with st.chat_message("ai"):
    st.markdown("Hi! I'm your AI assistant.")

# Display chat messages from history on app rerun
for role, message in st.session_state.messages:
    if role == "system":
        continue
    with st.chat_message(role):
        st.markdown(message)

current_chat_message = st.container()
prompt = st.chat_input("Ask your question here...", disabled=st.session_state.disabled)

if prompt:
    chat(prompt)
