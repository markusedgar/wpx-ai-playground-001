import streamlit as st
from langchain.llms import OpenAI
from langchain.schema import ChatMessage
from langchain import PromptTemplate

st.set_page_config(page_title="Draft an assumption-based future-state journey", page_icon=":robot:")


with st.sidebar:
   "This is an experimental space for the TiSDD training. Do not use with real project data."
   gptversion = 'gpt-3.5-turbo' # default: gpt-3.5-turbo
   gptversion = st.selectbox(
    'Choose ChatGPT version',
    ('gpt-3.5-turbo', 'gpt-4', 'gpt-4-0613'))
    # openai_api_key = st.text_input("OpenAI API Key", type="password")
   
openai_api_key = st.secrets.wpxspecial.OPENAIAPIKEY

journey_template = """
    Below is a description of a new service business concept, a target audience (as a persona description), and a scope to look at.      
    
    PERSONA/MAIN ACTOR: 
    {persona_input}

    CONCEPT: 
    {concept_input}

    In at least 10 steps, map out the experience journey of the persona/main actor end-2-end, from becoming aware of the concept to cancelling and returning back as a client in the future.

    
    For each step create
    * title. 
    * description. Description of activities and experiences at a step in about 50 words. Use {perspective_input} for any descriptions.

    Output the journey map as a markdown table with one column for each step. Use the format:

    (title) | (title) | (title) | (title) | …
    --- | --- | --- | --- | --- 
    ( description) | (description) | (description) | (description) | …
    ( label) | (label) | (label) | (label) | … """

prompt = PromptTemplate.from_template(journey_template)

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
            with st.spinner('Please wait...'):
                # prepare the prompt
                prompt_text = prompt.format_prompt(
                persona_input=persona_input, concept_input=concept_input,perspective_input=perspective_input
                )
                # Initialize the OpenAI module, load and run the summarize chain
                llm = OpenAI(openai_api_key=openai_api_key)
                llm_result = llm.generate(prompt_text)
            st.success(llm_result)
            