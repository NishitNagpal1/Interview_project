import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert
from my_codebase1 import engine, questions_table, async_session  # Correct imports

async def seed_data():
    try:
        # Create the database connection
        async with AsyncSession(engine) as session:
            async with session.begin():
                print("Connected to database")
                
                # Insert data into the table
                data = [
                    {
                        "question": "What is 2 + 2?",
                        "options": ["1", "2", "3", "4"],
                        "answer": "4",
                    },
                    {
                        "question": "What is the capital of France?",
                        "options": ["Paris", "London", "Berlin", "Madrid"],
                        "answer": "Paris",
                    },
                ]
                
                query = insert(questions_table).values(data)
                await session.execute(query)
                print("Data inserted successfully")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Ensure the database connection is closed
        await engine.dispose()
        print("Database connection closed")

if __name__ == "__main__":
    asyncio.run(seed_data())
