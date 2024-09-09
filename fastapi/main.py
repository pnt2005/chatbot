from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
import models, llm, pusher # type: ignore
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

class AnswerBase(BaseModel):
    text: str

class QuestionBase(BaseModel):
    text: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
    
@app.get('/questions')
async def get_question(db: db_dependency):
    result = db.query(models.Questions).all()
    if not result:
        raise HTTPException(status_code=404, detail='question is not found')
    return result

@app.get('/answers')
async def get_answer(db: db_dependency):
    result = db.query(models.Answers).all()
    if not result:
        raise HTTPException(status_code=404, detail='answer is not found')
    return result

pusher_client = pusher.Pusher(
    app_id=os.getenv('APP_ID'),
    key=os.getenv('KEY'),
    secret=os.getenv('SECRET'),
    cluster=os.getenv('CLUSTER'),
    ssl=True
)

@app.post('/chat')
async def post_chat(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    answer = llm.response(question.text)
    db_answer = models.Answers(text=answer)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)

    pusher_client.trigger('my-channel', 'my-event', {'message': answer})
