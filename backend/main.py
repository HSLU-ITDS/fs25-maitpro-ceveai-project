import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize FastAPI
app = FastAPI()


@app.post("/stream")
async def stream():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "Write a one-sentence bedtime story about a unicorn.",
                }
            ],
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
