from langchain.schema.runnable import RunnableParallel
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv

# Load environment variables (API key)
load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# Define prompts
company_prompt = PromptTemplate.from_template("Suggest a company name for a {business}.")
tagline_prompt = PromptTemplate.from_template("Create a tagline for {company}.")

company_chain = company_prompt | llm  # Chain for company name
tagline_chain = tagline_prompt | llm  # Chain for tagline

# Run company chain first to get the company name
company_result = company_chain.invoke({"business": "coffee shop"})
company_name = company_result.content  # Extract company name

# Run tagline chain using the generated company name
tagline_result = tagline_chain.invoke({"company": company_name})

# Print results
print("Company Name:", company_name)
print("Tagline:", tagline_result.content)
