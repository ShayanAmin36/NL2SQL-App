import sqlglot

def is_safe_sql(query: str) -> bool:
    """
    Reads the SQL query and ensures it is ONLY asking for data (SELECT),
    not trying to change or delete data.
    """
    try:
        # sqlglot breaks the SQL down into its grammatical parts
        parsed = sqlglot.parse(query)
        
        for expression in parsed:
            # If the main action isn't a "Select" statement, block it!
            if not isinstance(expression, sqlglot.expressions.Select):
                return False
        return True
    except Exception as e:
        # If the tool can't even understand the SQL, it's broken/unsafe.
        return False