import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, Form, File
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from llmservice import get_llm_service

# Load environment variables
load_dotenv()

# Initialize LLM service
llm_service = get_llm_service()

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
        messages = [
            {
                "role": "user",
                "content": "Write a one-sentence bedtime story about a unicorn.",
            }
        ]
        response = llm_service.generate_response(messages)
        print(response)
        return {"response": response}
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
    
