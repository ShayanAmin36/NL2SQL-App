from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database_utils import get_database_schema, execute_query
from security import is_safe_sql
from llm_engine import generate_sql

# Initialize the FastAPI application
app = FastAPI(title="NL2SQL API")


@app.get("/")
def root():
    return {
        "message": "NL2SQL API is running.",
        "docs": "/docs",
        "ask_endpoint": "/ask"
    }

# Define what the incoming data should look like
# We expect a JSON object with a single text field called "question"
class UserQuery(BaseModel):
    question: str

# Create a web endpoint that listens for POST requests at the URL path "/ask"
@app.post("/ask")
def ask_database(query: UserQuery):
    try:
        # Step A: Get the database blueprint
        schema = get_database_schema()

        # Step B: Ask the AI to write the SQL based on the user's question
        generated_sql = generate_sql(query.question, schema)
    except Exception as exc:
        # Return a clear error to the UI when LLM setup/config fails.
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate SQL: {str(exc)}"
        )
    
    # Step C: Send the AI's SQL to our security guard. 
    # If it fails, raise a 400 Bad Request error and stop immediately.
    if not is_safe_sql(generated_sql):
        raise HTTPException(status_code=400, detail="Generated SQL is unsafe or invalid.")
    
    # Step D: Run the safe SQL query against the Chinook database
    execution_result = execute_query(generated_sql)
    
    # Step E: Check if the database threw an error (like a column not existing)
    if not execution_result["success"]:
        return {
            "question": query.question,
            "sql": generated_sql,
            "error": execution_result["error"]
        }
    
    # Step F: If everything went perfectly, return the data!
    return {
        "question": query.question,
        "sql": generated_sql,
        "data": execution_result["data"]
    }