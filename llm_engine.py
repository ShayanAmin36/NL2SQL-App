from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# This acts like a key turning in a lock. It reads your .env file 
# and safely loads your GOOGLE_API_KEY into the system's memory.
load_dotenv() 

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file.")

# We initialize the "Brain". We are using Gemini 1.5 Flash here because it is fast and smart.
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GOOGLE_API_KEY,
)

# Think of a Prompt Template like a game of Mad Libs. 
# We write the instructions, and leave {blanks} for the dynamic pieces of information.
prompt_template = PromptTemplate.from_template(
    """
    You are an expert SQL Data Analyst.
    Given the following database schema, write a valid SQLite query to answer the user's question.
    Only return the SQL query, without any markdown formatting or explanations.

    Schema:
    {schema}

    Question: {question}

    SQL Query:
    """
)

def generate_sql(question: str, schema: str) -> str:
    """
    Takes the user's question and the database blueprint, 
    fills in the blanks of our prompt template, and asks the AI for the SQL.
    """
    # 1. Fill in the {schema} and {question} blanks in our template
    prompt = prompt_template.format(schema=schema, question=question)
    
    # 2. Send the filled-out prompt to the AI and wait for its answer
    response = llm.invoke(prompt)
    
    # 3. Clean up the AI's answer. 
    # AIs love to wrap code in markdown blocks like ```sql ... ```. 
    # Our database can't read markdown, so we must strip those out.
    clean_sql = response.content.replace("```sql", "").replace("```", "").strip()
    
    return clean_sql