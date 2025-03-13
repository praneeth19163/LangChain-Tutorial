from langchain.schema.runnable import RunnableParallel
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv, find_dotenv

# Load API Key
load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# Define prompt templates for two different tasks
summary_prompt = PromptTemplate.from_template("Summarize the following text: {text} in 5 words.")
keyword_prompt = PromptTemplate.from_template("Extract the important keywords from this text: {text}")

# Create independent chains
summary_chain = summary_prompt | llm
keyword_chain = keyword_prompt | llm

# Create a parallel chain that runs both tasks at the same time
parallel_chain = RunnableParallel({
    "summary": summary_chain,
    "keywords": keyword_chain
})

# Input text
input_text = "Artificial Intelligence (AI) is revolutionizing industries by enabling machines to learn from data and make decisions."

# Execute parallel chain
result = parallel_chain.invoke({"text": input_text})

# Print results
print("Summary:", result["summary"].content)
print("Keywords:", result["keywords"].content)
