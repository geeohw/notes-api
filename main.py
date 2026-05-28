import anthropic
from dotenv import load_dotenv
import os
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from auth import hash_password, verify_password, create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

class NoteCreate(BaseModel):
    body: str

class UserCreate(BaseModel):
    username: str
    password: str


def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/notes")
def get_notes(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(models.Note).all()

@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_note = models.Note(body=note.body)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        return {"error": "Note not found"}
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}

@app.post("/notes/{note_id}/optimize")
def optimize_note(note_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"I have the following tasks and notes for my day: {db_note.body}. Please analyze them and suggest an optimized daily schedule with time blocks, priorities, and reasoning for the order."
            }
        ]
    )
    
    return {
        "note": db_note.body,
        "optimized_schedule": message.content[0].text # type: ignore
    }

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(form_data.password, db_user.hashed_password): # type: ignore
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}