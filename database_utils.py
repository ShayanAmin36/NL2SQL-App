from sqlalchemy import create_engine, text
import pandas as pd

# This tells Python exactly where to find your database file
DATABASE_URL = "sqlite:///data/chinook.db"

# The "engine" is the actual connection cable between Python and the database
engine = create_engine(DATABASE_URL)

def get_database_schema() -> str:
    """
    Grabs the blueprint of the database (table names, column names)
    so we can show it to the AI.
    """
    # This is a special SQLite command that lists all tables and how they were created
    query = """
    SELECT type, name, sql 
    FROM sqlite_master 
    WHERE type='table';
    """
    
    # We use pandas to run the query and easily organize the results
    df = pd.read_sql(query, engine)
    
    # We stitch all the table blueprints into one giant text string
    schema_text = "\n".join(df['sql'].dropna().tolist())
    return schema_text

def execute_query(query: str):
    """
    Takes a safe SQL string, runs it against the database, 
    and returns the rows of data.
    """
    try:
        # Open a connection using our engine
        with engine.connect() as connection:
            # Run the SQL query
            result = connection.execute(text(query))
            
            # Convert the raw database rows into standard Python dictionaries
            rows = [dict(row._mapping) for row in result]
            
            # Return a success message and the data
            return {"success": True, "data": rows}
            
    except Exception as e:
        # If the database throws an error, catch it gracefully so the app doesn't crash
        return {"success": False, "error": str(e)}