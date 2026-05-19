from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class NoteCreate(BaseModel):
    body: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(body=note.body)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        return {"error": "Note not found"}
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}