from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import random
from fastapi.middleware.cors import CORSMiddleware


DATABASE_URL = "postgresql+asyncpg://postgres:Nishit%4012@localhost:5432/question_bank"



# Set up the FastAPI app
app = FastAPI()


# Allow all origins (you can replace '*' with specific domains if you want to restrict)
origins = [
    "http://localhost:3000",  
]

# Add CORSMiddleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Example endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
# Set up the database and metadata for SQLAlchemy
metadata = MetaData()

questions_table = Table(
    "questions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("question", String, nullable=False),
    Column("options", JSON, nullable=False),
    Column("answer", String, nullable=False),
)

# Create the async SQLAlchemy engine and sessionmaker
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Pydantic model for answer submission
class AnswerSubmission(BaseModel):
    question_id: int
    submitted_answer: str

# FastAPI event handlers to connect and disconnect from the database
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

# Endpoint to get random questions
@app.get("/questions")
async def get_random_questions(count: int = 1):
    """
    Fetch `count` random questions from the database.
    """
    async with async_session() as session:
        result = await session.execute(select(questions_table))
        rows = result.fetchall()
        all_questions = [{"id": row.id, "question": row.question, "options": row.options, "answer": row.answer} for row in rows]

        if count > len(all_questions):
            count = len(all_questions)
        random_questions = random.sample(all_questions, count)
        return {"questions": random_questions}

# Endpoint to submit an answer
@app.post("/submit")
async def submit_answer(answer: AnswerSubmission):
    async with async_session() as session:
        query = select(questions_table).where(questions_table.c.id == answer.question_id)
        result = await session.execute(query)
        question = result.fetchone()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        correct = question["answer"] == answer.submitted_answer
        return {"correct": correct}
