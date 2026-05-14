from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
notes = []

class Note(BaseModel):
    id: int
    body: str

@app.post("/notes")
def create_note(note: Note):
    notes.append(note)
    return note

@app.get("/notes")
def get_notes():
    return notes

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    global notes
    notes = [note for note in notes if note.id != note_id]
    return {"message": f"Note with id {note_id} deleted"}