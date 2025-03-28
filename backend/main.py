import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, Form, File
from openai import OpenAI
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

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
    
@app.post("/upload-preview")
async def upload_preview(
    files: List[UploadFile] = File(...),
    prompt: str = Form(...)
):
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")

        files_info = []

        for file in files:
            # Validate file type by extension and content type
            if not file.filename.lower().endswith(".pdf") or file.content_type != "application/pdf":
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' is not a valid PDF"
                )

            content = await file.read()
            files_info.append({
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content)
            })

        return {
            "status": "success",
            "message": f"{len(files)} PDF file(s) received successfully",
            "files": files_info,
            "prompt": prompt
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
