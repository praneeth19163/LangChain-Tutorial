import os
import sqlite3

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm=ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

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

    return history


create_database()
history_for_chain = load_history()

prompt_template = ChatPromptTemplate.from_messages([
    ("system",  "You are a python Expert.Answer any questions "
              "related to the Python ,if they ask about any program give the code properly with proper identation and list all the packages in code correctly.if the question is not related to agile return applogy kind of message"),
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

print("Python Guide")

while True:
    question = input("Enter the question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        print("Exiting chat...")
        break

    if question:
        save_to_database("human", question)
        response = chain_with_history.invoke({"input": question}, {"configurable": {"session_id": "abc123"}})
        save_to_database("ai", response.content)
        print(response.content)
