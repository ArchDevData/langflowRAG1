import streamlit as st
from langflow.load import run_flow_from_json
from typing import Optional

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

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  api_key: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def chat(prompt: str):
  with current_chat_message:
    # Block input to prevent sending messages whilst AI is responding
    st.session_state.disabled = True

    # Add user message to chat history
    st.session_state.messages.append(("human", prompt))

    # Display user message in chat message container
    with st.chat_message("human"):
      st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("ai"):
      # Get complete chat history, including latest question as last message
      history = "\n".join(
        [f"{role}: {msg}" for role, msg in st.session_state.messages]
      )

      query = f"{history}\nAI:"

      # Setup any tweaks you want to apply to the flow
      inputs = {"question": query}

      # output = run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS)
      flow = run_flow_from_json(flow="./LangRAG.json", input_value=inputs, tweaks=TWEAKS)
      output = flow(inputs)
      print("output from the model is: ")
      print(output)
      try:
        output = output['chat_history'][-1].content
      except Exception :
        output = f"Application error : {output}"

      placeholder = st.empty()

      # write response without "▌" to indicate completed message.
      with placeholder:
        st.markdown(output)

    # Log AI response to chat history
    st.session_state.messages.append(("ai", output))
    # Unblock chat input
    st.session_state.disabled = False

    st.rerun()


st.set_page_config(page_title="AI for AI")
st.title("Chat RAG")

system_prompt = "You´re a helpful assistant who can explain concepts"
if "messages" not in st.session_state:
    st.session_state.messages = [("system", system_prompt)]
if "disabled" not in st.session_state:
    # `disable` flag to prevent user from sending messages whilst the AI is responding
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

