import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
DB_NAME = "chat_history.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_database(role, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (role, message) VALUES (?, ?)", (role, message))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT role, message FROM chat_history")
    rows = cursor.fetchall()
    conn.close()

    history = ChatMessageHistory()
    for role, message in rows:
        if role == "human":
            history.add_user_message(message)
        elif role == "ai":
            history.add_ai_message(message)

    return history, rows

create_database()
history_for_chain, chat_history_rows = load_history()

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a Python Expert. Answer any questions "
               "related to Python. If a user asks for a program, provide properly formatted code with necessary package details. If the question is unrelated, return an apology."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
chain = prompt_template | llm
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history"
)

st.title("Python Guide Chatbot 🤖")

if "show_history" not in st.session_state:
    st.session_state.show_history = False

if st.button("Show/Hide Chat History"):
    st.session_state.show_history = not st.session_state.show_history

if st.session_state.show_history:
    st.subheader("Chat History")
    for role, message in chat_history_rows:
        st.write(f"**{role.capitalize()}**: {message}")

question = st.text_input("Ask your Python-related question:")

if st.button("Submit"):
    if question:
        save_to_database("human", question)
        response = chain_with_history.invoke({"input": question}, {"configurable": {"session_id": "abc123"}})
        save_to_database("ai", response.content)
        st.subheader("Response:")
        st.write(response.content)
