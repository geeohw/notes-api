# Notes API

A REST API built with FastAPI and Python that allows users to create, 
retrieve, and delete notes.

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | /notes | Retrieve all notes |
| POST | /notes | Create a new note |
| DELETE | /notes/{id} | Delete a note by ID |

## Tech Stack

- Python
- FastAPI
- Uvicorn

## How to Run

1. Install dependencies:
pip install fastapi uvicorn

2. Start the server:
python -m uvicorn main:app --reload

3. Visit http://127.0.0.1:8000/docs to test the API interactively