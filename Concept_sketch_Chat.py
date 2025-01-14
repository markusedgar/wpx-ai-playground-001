from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain import ChatPromptTemplate
import streamlit as st

st.set_page_config(page_title="Draft an assumption-based future-state journey", page_icon=":robot:")

with st.sidebar:
   "This is an experimental space for the TiSDD training. Do not use with real project data."
   gptversion = 'gpt-3.5-turbo' # default: gpt-3.5-turbo
   gptversion = st.selectbox('Choose ChatGPT version', ('gpt-3.5-turbo', 'gpt-4', 'gpt-4-0613'))
   openai_api_key = st.secrets.wpxspecial.OPENAIAPIKEY

system_template = """You are a helpful assistant."""
system_message_prompt = ChatPromptTemplate.from_template(system_template)

journey_template = """
    Please provide a table listing the steps of the persona's experience with the service in columns from left to right in markdown format:    
    
    PERSONA/MAIN ACTOR: 
    {persona_input}

    SERVICE CONCEPT: 
    {concept_input}

    Focus on the end-2-end experience of that service concept (from becoming aware of the service to Renewing the contract or returning.)
    For each step create a description of activities and experiences in about 50 words. Use {perspective_input} language.

"""

human_message_prompt = ChatPromptTemplate.from_template(journey_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

st.write(chat_prompt)

st.header("TiSDD Journey Map Generator")

def get_persona():
    input_text = st.text_area(label="Persona input", label_visibility='collapsed', placeholder="Your persona...", key="persona_input")
    return input_text

def get_concept():
    input_text = st.text_area(label="Concept input", label_visibility='collapsed', placeholder="Your concept...", key="concept_input")
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
     
    submit_button = st.form_submit_button(label='Generate journey draft')
    if submit_button:
         with st.spinner('Please wait...'):
            st.markdown("### Your Journey Draft:")
            # prepare the prompt
            st.write(chat_prompt.format_prompt(persona_input=persona_input, concept_input=concept_input,perspective_input=perspective_input))
            #llm = ChatOpenAI(openai_api_key=openai_api_key, model=gptversion)
            #response = llm(chat_prompt.format_prompt(persona_input=persona_input, concept_input=concept_input,perspective_input=perspective_input))
            st.write("Test")
