import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from langchain import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate)

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

system_template = "You are a helpful assistant supports creating business concepts through a This is Service Design Doing like approach."
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template = """
    Below is a description of a new service business concept, a target audience (as a persona description), and a scope to look at.      
    
    PERSONA/MAIN ACTOR: 
    {persona_input}

    CONCEPT: 
    {concept_input}

    SCOPE: 
    {scope_input}

    For the given concept create customer experience as a step-by-step journey map as a table with one column for each step.
    Use {perspective_input} for any description. Use emotional language where appropriate.

    For each step create:

    * title. 
    * description. Description of activities and experiences of the given persona at this step in not longer than 50 words.
 
    Output the journey map as a markdown table with one column for each step. Use the format:

    (title) | (title) | (title) | (title) | …
    --- | --- | --- | --- | --- 
    ( description) | (description) | (description) | (description) | …
    ( label) | (label) | (label) | (label) | … """

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

## prompt=PromptTemplate(
##    template=humanTemplate,
##    input_variables=["persona_input", "concept_input", "scope_input", "perspective_input"],
## )

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

## humanMessagePrompt = ChatPromptTemplate(
##    input_variables=["persona", "concept", "scope", "person_select"],
##    template=template,
## )

st.header("TiSDD Journey Map Generator")

st.markdown("# Some heading 3")


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

    st.markdown("### Perspective")
    perspective_input = st.selectbox(
        'Which perspective would you like to use for the journey?',
        ('first person (me, myself, I)', 'third person (he/she/them)'))

    st.markdown("### Persona/Main actor")
    persona_input = get_persona()

    st.markdown("### Concept summary")
    concept_input = get_concept()

    st.markdown("### Scope")
    scope_input = get_scope()
     
    submit_button = st.form_submit_button(label='Generate journey draft')
    if submit_button:
         with st.spinner('Please wait...'):
            st.markdown("### Your Journey Draft:")

            prompt_text = chat_prompt.format_prompt(
            persona_input=persona_input, concept_input=concept_input,scope_input=scope_input, perspective_input=perspective_input
            ).to_messages()
