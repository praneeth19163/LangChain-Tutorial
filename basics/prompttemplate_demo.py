import os
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv(),override=True)
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')


llm=ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
prompt_template = PromptTemplate(
    input_variables=["country","no_of_paras","language"],
    template="""You are an expert in traditional cuisines.
    You provide information about a specific dish from a specific country.
    Avoid giving information about fictional places. If the country is fictional
    or non-existent answer: I don't know.
    Answer the question: What is the traditional cuisine of {country}?
    Answer in {no_of_paras} short paras in {language}
    """
)

st.title("Cuisine Info")

country = st.text_input("Enter the country:")
no_of_paras = st.number_input("Enter the number of paras",min_value=1,max_value=5)
language = st.text_input("Enter the language:")

if country:
    response = llm.invoke(prompt_template.format(country=country,
                                                 no_of_paras=no_of_paras,
                                                 language=language
                                                 ))
    st.write(response.content)
#
# import os
# from langchain_openai import ChatOpenAI
# import streamlit as st
# from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
# from dotenv import load_dotenv, find_dotenv
#
# # Load API key
# load_dotenv(find_dotenv(), override=True)
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
#
# # Define the LLM model
# llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
#
# # Define the chat prompt template with roles
# prompt_template = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate.from_template(
#         "You are an expert in traditional cuisines. You provide information about dishes from different countries. "
#         "Avoid fictional places. If the country is fictional, respond: 'I don't know.'"
#     ),
#     HumanMessagePromptTemplate.from_template(
#         "What is the traditional cuisine of {country}? Provide the answer in {no_of_paras} short paragraphs in {language}."
#     )
# ])
#
# # Streamlit UI
# st.title("Cuisine Info")
#
# country = st.text_input("Enter the country:")
# no_of_paras = st.number_input("Enter the number of paragraphs", min_value=1, max_value=5)
# language = st.text_input("Enter the language:")
#
# if country:
#     # Format the structured prompt
#     messages = prompt_template.format_messages(country=country, no_of_paras=no_of_paras, language=language)
#
#     # Invoke LLM with the structured chat messages
#     response = llm.invoke(messages)
#
#     st.write(response.content)
