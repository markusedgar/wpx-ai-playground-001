from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


with st.sidebar:
   "This is an experimental space for the TiSDD training. Do not use with real project data."
   gptversion = 'gpt-3.5-turbo' # default: gpt-3.5-turbo
   gptversion = st.selectbox(
    'Choose ChatGPT version',
    ('gpt-3.5-turbo', 'gpt-4', 'gpt-4-0613'))
    # openai_api_key = st.text_input("OpenAI API Key", type="password")
   
openai_api_key = st.secrets.wpxspecial.OPENAIAPIKEY

st.title('TiSDD Helper Chat ')

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]


for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=openai_api_key, model=gptversion, streaming=True, callbacks=[stream_handler])
        response = llm(st.session_state.messages)
        st.text(st.session_state.messages)
        st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))