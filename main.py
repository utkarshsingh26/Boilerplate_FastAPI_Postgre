from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from repository import QuizRepository
from service import QuizService
from pydantic import BaseModel
from typing import List

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_quiz_service(db: Session = Depends(get_db)):
    repo = QuizRepository(db)
    return QuizService(repo)

# Routes
@app.get("/questions/{question_id}")
async def read_question(question_id: int, service: QuizService = Depends(get_quiz_service)):
    result = service.get_question_with_choices(question_id)
    if not result:
        raise HTTPException(status_code=404, detail='Question not found')
    return result

@app.post("/questions")
async def create_questions(question: QuestionBase, service: QuizService = Depends(get_quiz_service)):
    return service.create_full_question(question)
