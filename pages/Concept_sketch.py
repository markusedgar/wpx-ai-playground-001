import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from langchain import PromptTemplate
from langchain.llms import OpenAI
 
st.set_page_config(page_title="Draft an assumption-based future-state journey", page_icon=":robot:")

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


template = """
    Below is a description of a new service business concept, a target audience (as a persona description), and a scope to look at.      
    
    PERSONA: 
    {persona}

    CONCEPT: 
    {concept}

    SCOPE: 
    {scope}

    For the given concept create customer experience as a step-by-step journey map as a table with one column for each step.
    Use {person_select} for any description. Use emotional language where appropriate.

    For each step create:

    * title. 
    * description. Description of activities and experiences of the given persona at this step in not longer than 50 words.
    * label. Label the step based on those three labels: 
        * DIRECT for direct touchpoints (iteracting with the provider, e.g. meeting, workshop or phone call)
        * INDIRECT for indirect touchpoint (indirectly interacting with the provider or with information about the provider, e.g. review sites, word of mouth)
        * INTERNAL for internal step (not interacting with the provider, e.g. when making internal decisions, comparing alternatives, finding budgets etc.)

    Output the journey map as a markdown table with one column for each step. Use the format:

    (title) | (title) | (title) | (title) | …
    --- | --- | --- | --- | --- 
    ( description) | (description) | (description) | (description) | …
    ( label) | (label) | (label) | (label) | …

"""

prompt = PromptTemplate(
    input_variables=["persona", "concept", "scope", "person_select"],
    template=template,
)

st.write(prompt)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(openai_api_key=openai_api_key)
    return llm

st.header("TiSDD Journey Map Generator")

st.markdown("# Some heading 2")


def get_persona():
    input_text = st.text_area(label="Persona input", label_visibility='collapsed', placeholder="Your persona...", key="persona_input")
    return input_text

def get_concept():
    input_text = st.text_area(label="Concept input", label_visibility='collapsed', placeholder="Your concept...", key="concept_input")
    return input_text

def get_scope():
    input_text = st.text_area(label="Scope input", label_visibility='collapsed', placeholder="Your scope...", key="scope_input")
    return input_text


with st.form(key='journey_input_form'):

    st.markdown("## Perspective")
    option_person = st.selectbox(
        'Which perspective would you like to use for the journey?',
        ('first person (me, myself, I)', 'third person (he/she/them)'))

    st.markdown("## Persona")
    persona_input = get_persona()

    st.markdown("## Concept summary")
    concept_input = get_concept()

    st.markdown("## Scope")
    scope_input = get_scope()
    
    submit_button = st.form_submit_button(label='Generate journey draft')


## if len(concept_input.split(" ")) > 100:
##     st.write("Please enter a shorter scope. The maximum length is 100 words.")
##     st.stop()

## if len(concept_input.split(" ")) > 500:
##     st.write("Please enter a shorter concept description. The maximum length is 500 words.")
##    st.stop()

st.markdown("### Your Journey Draft:")


if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="Let's get to work.")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)


st.session_state.messages.append(ChatMessage(role="user", content=prompt))

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=openai_api_key, model=gptversion, streaming=True, callbacks=[stream_handler])
        response = llm(st.session_state.messages)
        st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))
