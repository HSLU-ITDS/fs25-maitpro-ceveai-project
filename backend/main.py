import os
import logging
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, Form, File
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from llmservice import get_llm_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()  # This will also print to console
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Initialize LLM service
try:
    llm_service = get_llm_service()
    logger.info("LLM service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLM service: {str(e)}")
    raise

# Initialize FastAPI
app = FastAPI()
logger.info("FastAPI application initialized")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
logger.info("CORS middleware configured")

@app.post("/stream")
async def stream():
    try:
        logger.info("Received stream request")
        messages = [
            {
                "role": "user",
                "content": "Write a one-sentence bedtime story about a unicorn.",
            }
        ]
        response = llm_service.generate_response(messages)
        logger.info("Successfully generated response")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error in stream endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload-preview")
async def upload_preview(
    files: List[UploadFile] = File(...),
    prompt: str = Form(...)
):
    try:
        logger.info(f"Received upload-preview request with {len(files)} files")
        if not files:
            logger.warning("No files provided in request")
            raise HTTPException(status_code=400, detail="No files provided")

        files_info = []

        for file in files:
            # Validate file type by extension and content type
            if not file.filename.lower().endswith(".pdf") or file.content_type != "application/pdf":
                logger.warning(f"Invalid file type: {file.filename}")
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
            logger.info(f"Processed file: {file.filename}")

        logger.info("Successfully processed all files")
        

        return {
            "status": "success",
            "message": f"{len(files)} PDF file(s) received successfully",
            "files": files_info,
            "prompt": prompt
        }

    except Exception as e:
        logger.error(f"Error in upload-preview endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
