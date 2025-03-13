# import os
# from langchain_openai import ChatOpenAI
# import streamlit as st
# from langchain.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
# from dotenv import load_dotenv, find_dotenv
# from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
# load_dotenv(find_dotenv(), override=True)
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# llm=ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
# title_prompt = PromptTemplate(
#     input_variables=["topic"],
#     template="""You are an experienced speech writer.
#     You need to craft an impactful title for a speech
#     on the following topic: {topic}
#     Answer exactly with one title.
#     """
# )
#
# speech_prompt = PromptTemplate(
#     input_variables=["title", "emotion"],
#     template="""You need to write a powerful {emotion} speech of 350 words
#      for the following title: {title}
#      format the output with 2 keys:"title","speech" and fill them
#      with the respective values.
#     """
# )
#
# first_chain = title_prompt | llm | StrOutputParser() | (lambda title: (st.write(title),title)[1])
# second_chain = speech_prompt | llm | JsonOutputParser
# final_chain = first_chain | (lambda title:{"title": title,"emotion": emotion}) | second_chain
#
# st.title("Speech Generator")
#
# topic = st.text_input("Enter the topic:")
# emotion = st.text_input("Enter the emotion:")
#
# if topic and emotion:
#     response = final_chain.invoke({"topic":topic})
#     st.write(response)
#
import os
from langchain_openai import ChatOpenAI
from basics import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="You are an experienced speech writer. Suggest an impactful title for a speech on {topic}. Answer exactly with one title."
)

speech_prompt = PromptTemplate(
    input_variables=["title", "emotion"],
    template="""Write a {emotion} speech of 350 words for the title: {title}.
    Format the output as a JSON with keys: "title" and "speech","emotion".
    emotion key should i consist {emotion}.
    """
)

first_chain = title_prompt | llm | StrOutputParser()
second_chain = speech_prompt | llm | JsonOutputParser()  # Sequential Execution
def generate_speech(topic, emotion):
    title = first_chain.invoke({"topic": topic})
    result = second_chain.invoke({"title": title, "emotion": emotion})
    return result


st.title("Speech Generator")

topic = st.text_input("Enter the topic:")
emotion = st.text_input("Enter the emotion:")

if topic and emotion:
    response = generate_speech(topic, emotion)
    st.write(response)
