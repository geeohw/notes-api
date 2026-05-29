# Notes API

An AI-powered REST API built with FastAPI and Python that allows users to create,
retrieve, and delete notes — with built-in AI schedule optimization powered by Google Gemini.

## Features

- JWT authentication with bcrypt password hashing
- Full CRUD operations for note management
- AI-powered daily schedule optimization
- Persistent SQLite database via SQLAlchemy

## Endpoints

| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| POST | /register | Register a new user | No |
| POST | /login | Login and receive JWT token | No |
| GET | /notes | Retrieve all notes | Yes |
| POST | /notes | Create a new note | Yes |
| DELETE | /notes/{id} | Delete a note by ID | Yes |
| POST | /notes/{id}/optimize | Optimize daily schedule using AI | Yes |

## Tech Stack

- Python
- FastAPI
- Uvicorn
- SQLAlchemy + SQLite
- JWT Authentication (python-jose)
- Password Hashing (bcrypt)
- Google Gemini AI

## How to Run

1. Clone the repository:
git clone https://github.com/geeohw/notes-api.git

2. Install dependencies:
pip install fastapi uvicorn sqlalchemy python-jose passlib bcrypt google-genai python-dotenv

3. Create a .env file with your Gemini API key:
GEMINI_API_KEY=your_key_here

4. Start the server:
python -m uvicorn main:app --reload

5. Visit http://127.0.0.1:8000/docs to test the API interactively