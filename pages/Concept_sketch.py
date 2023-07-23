import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
 
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

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Draft an assumption-based future-state journey", page_icon=":robot:")
st.header("TiSDD Journey Map Generator")

st.markdown("# Some heading")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = st.secrets.wpxspecial.OPENAIAPIKEY


def get_persona():
    input_text = st.text_area(label="Persona input", label_visibility='collapsed', placeholder="Your persona...", key="persona_input")
    return input_text

def get_concept():
    input_text = st.text_area(label="Concept input", label_visibility='collapsed', placeholder="Your concept...", key="concept_input")
    return input_text

def get_scope():
    input_text = st.text_area(label="Scope input", label_visibility='collapsed', placeholder="Your scope...", key="scope_input")
    return input_text


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



if len(concept_input.split(" ")) > 100:
    st.write("Please enter a shorter scope. The maximum length is 100 words.")
    st.stop()

if len(concept_input.split(" ")) > 500:
    st.write("Please enter a shorter concept description. The maximum length is 500 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Journey Draft:")

if concept_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = OpenAI(openai_api_key=openai_api_key)

    prompt_with_concept = prompt.format(persona=persona_input, concept=concept_input, scope=scope_input, person_select=option_person)

    journey_draft = llm(prompt_with_concept)

    st.markdown(journey_draft)