import streamlit as st
from typing import Optional

from langflow.load import run_flow_from_json  # Updated import


TWEAKS = {
  "PyPDFLoader-meyB2": {},
  "RecursiveCharacterTextSplitter-aIe6R": {},
  "OllamaEmbeddings-FzJxP": {},
  "BaseChatModel-uQUH3": {},
  "ConversationBufferMemory-adobv": {},
  "ConversationalRetrievalChain-RD8zz": {},
  "FAISS-I7M5T": {},
  "PyPDFLoader-BqluX": {},
  "PyPDFLoader-wBYkk": {},
  "PyPDFLoader-cvTr4": {}
}


def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param inputs: The inputs to the flow
    :param flow_id: The ID of the flow to run
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    flow = run_flow_from_json(flow_path="LangRAG.json", tweaks=tweaks)  # Updated function
    return flow(inputs)  # Adjusted to run the loaded flow


def chat(prompt: str):
    with current_chat_message:
        # Block input to prevent sending messages while AI is responding
        st.session_state.disabled = True

        # Add user message to chat history
        st.session_state.messages.append(("human", prompt))

        # Display user message in chat message container
        with st.chat_message("human"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("ai"):
            # Get complete chat history, including the latest question as the last message
            history = "\n".join(
                [f"{role}: {msg}" for role, msg in st.session_state.messages]
            )

            query = f"{history}\nAI:"

            # Set up any tweaks you want to apply to the flow
            inputs = {"question": query}

            try:
                output = run_flow(inputs, flow_id="FLOW_ID", tweaks=TWEAKS)
                print("Output from the model is:")
                print(output)

                # Parse the output
                output = output['chat_history'][-1].content
            except Exception as e:
                output = f"Application error: {e}"

            placeholder = st.empty()

            # Write response without "▌" to indicate a completed message.
            with placeholder:
                st.markdown(output)

        # Log AI response to chat history
        st.session_state.messages.append(("ai", output))
        # Unblock chat input
        st.session_state.disabled = False

        st.rerun()


# Streamlit setup
st.set_page_config(page_title="AI for AI")
st.title("Welcome to the AI explains AI world!")

system_prompt = "You´re a helpful assistant who can explain concepts"
if "messages" not in st.session_state:
    st.session_state.messages = [("system", system_prompt)]
if "disabled" not in st.session_state:
    # `disabled` flag to prevent user from sending messages while AI is responding
    st.session_state.disabled = False


with st.chat_message("ai"):
    st.markdown(
        f"Hi! I'm your AI assistant."
    )

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
