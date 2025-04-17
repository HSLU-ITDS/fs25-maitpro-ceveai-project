import os
import logging
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, Form, File
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from services.llm_service import get_llm_service
from services.ocr_services import OCRService

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


@app.post("/test-prompt")
async def test_prompt(prompt: str = Form(...)):
    """
    This endpoint is used to test the LLM service.
    It will return the response from the LLM given a prompt from the user.
    """
    try:
        logger.info(f"Received test-prompt request with prompt: {prompt}")
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        response = llm_service.generate_response(messages)
        logger.info(response)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error in test-prompt endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    
        
    
@app.post("/upload-preview")
async def upload_preview(
    files: List[UploadFile] = File(...),
):
    """
    This endpoint is used to upload a PDF file and return the metadata of the file.
    """
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
            "files": files_info
        }

    except Exception as e:
        logger.error(f"Error in upload-preview endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@app.post("/process-cv")
async def process_cv(file: UploadFile = File(...)):
    try:
        logger.info(f"Received CV processing request for file: {file.filename}")
        
        # Initialize OCR service
        ocr_service = OCRService()
        
        # Process the document using OCR service
        result = await ocr_service.parse_document(file)
        
        logger.info(result)
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error processing CV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

@app.post("/rank-cvs")
async def rank_cvs(
    files: List[UploadFile] = File(...),
    criteria: List[str] = Form(...)
):
    """
    This endpoint receives a list of CVs and user criteria, processes them,
    and returns a ranked list of CVs based on how well they match the criteria.
    """
    try:
        logger.info(f"Received rank-cvs request with {len(files)} files and criteria: {criteria}")
        
        if not files:
            logger.warning("No files provided in request")
            raise HTTPException(status_code=400, detail="No files provided")
            
        if not criteria:
            logger.warning("No criteria provided in request")
            raise HTTPException(status_code=400, detail="No criteria provided")
        
        # Initialize OCR service
        ocr_service = OCRService()
        
        # Process each CV and get their summaries
        cv_summaries = []
        for file in files:
            # Parse the document
            parsed_content = await ocr_service.parse_document(file)
            
            # Get the markdown content from the parsed result
            content = parsed_content.get("markdown_content", "")
            
            # Summarize the content against the criteria
            summary = await ocr_service.summarize_content(content, criteria)
            
            cv_summaries.append({
                "filename": file.filename,
                "summary": summary
            })
        
        # Rank the CVs based on their summaries
        ranked_cvs = await ocr_service.rank_cvs(cv_summaries, criteria)
        
        logger.info("Successfully ranked CVs")
        return {
            "status": "success",
            "ranked_cvs": ranked_cvs
        }
        
    except Exception as e:
        logger.error(f"Error in rank-cvs endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error ranking CVs: {str(e)}")





