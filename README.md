# NL2SQL-App

NL2SQL-App converts natural-language business questions into safe, executable SQLite queries and returns tabular results.

It includes:
- A FastAPI backend that generates SQL with Gemini via LangChain.
- A Streamlit frontend for asking questions and downloading results as CSV.
- A SQL safety layer using sqlglot to allow read-only queries.
- A local SQLite sample database (`Chinook`) for quick testing.

## Architecture

1. User asks a question in Streamlit.
2. Frontend calls `POST /ask` on FastAPI.
3. Backend loads DB schema and sends prompt to LLM.
4. Generated SQL is validated by the safety checker.
5. Safe SQL is executed against SQLite.
6. JSON response is shown as a table in Streamlit.

## Tech Stack

- Python
- FastAPI + Uvicorn
- Streamlit
- SQLAlchemy + SQLite
- LangChain + Google Gemini
- sqlglot
- pandas

## Project Structure

```
NL2SQL-App/
|-- app.py                 # Streamlit UI
|-- main.py                # FastAPI API
|-- llm_engine.py          # LLM prompt + SQL generation
|-- database_utils.py      # Schema fetch + query execution
|-- security.py            # SQL safety checks
|-- requirements.txt
|-- .env                   # Local secrets (not committed)
|-- data/
|   `-- chinook.db
`-- prompts/
```

## Prerequisites

- Python 3.10+
- A Google AI API key

## Setup

1. Clone the repository

```bash
git clone https://github.com/ShayanAmin69/NL2SQL-App.git
cd NL2SQL-App
```

2. Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root

```env
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

## Run The App

Open two terminals.

Terminal 1: start the API

```bash
uvicorn main:app --reload
```

Terminal 2: start Streamlit

```bash
streamlit run app.py
```

Then open the Streamlit URL shown in terminal (usually `http://localhost:8501`).

## API

### Health

`GET /`

Response:

```json
{
  "message": "NL2SQL API is running.",
  "docs": "/docs",
  "ask_endpoint": "/ask"
}
```

### Ask

`POST /ask`

Request body:

```json
{
  "question": "Show top 10 customers by total spending"
}
```

Success response shape:

```json
{
  "question": "...",
  "sql": "SELECT ...",
  "data": [
    {"column": "value"}
  ]
}
```

Failure response shape:

```json
{
  "question": "...",
  "sql": "...",
  "error": "database execution error"
}
```

## Safety Model

- SQL is parsed with `sqlglot`.
- Only `SELECT` statements are allowed.
- Invalid or unsafe SQL is rejected before execution.

## Example Questions

- Top 10 customers by total spend.
- Invoices per month.
- Best-selling artists.
- Most expensive tracks.

## Notes

- Keep `.env` private and never commit API keys.
- The current `requirements.txt` contains duplicate entries; this does not usually break installation, but you may clean it later.

## License

Add a license file (for example MIT) if you want explicit reuse terms.
