import sqlite3
import openai
import re  
client = openai.Client(api_key="s-proj-Zn969-jsKCD-JcOGWVzV14fKCoBBRfOeiJfg4mOd4OF2irLFFINxH8PyX3DapYEDmMkMWW80hsT3BlbkFJJX96QfzwQDNMgaMCsKi9Po7i2DCw1nqk1p5UMAVbH6MG3ZHuANAy40af1lj6DZlxz6LI77p0EA")


def clean_sql_query(raw_query):
    """
    Cleans the SQL query by removing Markdown formatting (like triple backticks).
    """
    cleaned_query = re.sub(r"```sql|```", "", raw_query, flags=re.MULTILINE).strip()
    return cleaned_query


def generate_sql_query(natural_language_query):
    """
    Converts a natural language question into a SQL query using GPT-4o.
    """
    prompt = f"""
    You are an AI assistant that converts natural language questions into SQL queries.
    The database has a table called 'employees' with these columns:
    - id (INTEGER, PRIMARY KEY)
    - name (TEXT)
    - mail (TEXT, UNIQUE)
    - domain (TEXT) [Example: 'Python', 'Java', 'JavaScript']
    - salary (INTEGER)

    Convert the following user question into an SQL query (without explanation):

    Question: "{natural_language_query}"

    SQL Query:
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are an expert SQL assistant. Output only the SQL query without backticks."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_sql_query = response.choices[0].message.content.strip()
    cleaned_sql_query = clean_sql_query(raw_sql_query)

    return cleaned_sql_query


def fetch_data_from_db(sql_query):
    """
    Executes the generated SQL query on the existing employee database and returns results.
    """
    conn = sqlite3.connect("employee.db")  
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()

        if results:
            return results
        else:
            return "No matching records found."

    except Exception as e:
        conn.close()
        return f"Error: {e}"


def chatbot_response(natural_query):
    """
    Handles user queries: converts to SQL, executes it, and returns results.
    """
    sql_query = generate_sql_query(natural_query)
    print(f"Generated SQL Query: {sql_query}")  
    results = fetch_data_from_db(sql_query)
    return results


user_query = input("enter the query in natural language:")
response = chatbot_response(user_query)

print("Results:", response)
