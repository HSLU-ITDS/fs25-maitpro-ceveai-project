import os
import logging
from datetime import datetime
import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, Form, File
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from services.llm_service import get_llm_service
from services.ocr_services import OCRService
#from services.pdf_service import PDFService

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

# @app.post("/stream")
# async def stream():
#     try:
#         logger.info("Received stream request")
#         messages = [
#             {
#                 "role": "user",
#                 "content": "Write a one-sentence bedtime story about a unicorn.",
#             }
#         ]
#         response = llm_service.generate_response(messages)
#         logger.info("Successfully generated response")
#         return {"response": response}
#     except Exception as e:
#         logger.error(f"Error in stream endpoint: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/test-input")
# async def test_input(
#     files: List[UploadFile] = File(...),
#     criteria: str = Form(...),
#     prompt: str = Form(None)
# ):
#     """
#     Test endpoint to receive PDF files, criteria, and job description, and display them clearly.
#     """
#     try:
#         logger.info(f"Received test-input request with {len(files)} files, criteria: {criteria}, and prompt: {prompt}")
#         if not files:
#             logger.warning("No files provided in request")
#             raise HTTPException(status_code=400, detail="No files provided")
#         if not criteria:
#             logger.warning("No criteria provided in request")
#             raise HTTPException(status_code=400, detail="No criteria provided")
#         if not prompt:
#             logger.warning("No prompt (job description) provided in request")
#             raise HTTPException(status_code=400, detail="No prompt (job description) provided")

#         # Parse criteria JSON
#         try:
#             parsed_criteria = json.loads(criteria)
#         except Exception as e:
#             logger.error(f"Failed to parse criteria JSON: {str(e)}")
#             raise HTTPException(status_code=400, detail="Invalid criteria JSON")

#         # Parse prompt JSON
#         parsed_prompt = None
#         if prompt:
#             try:
#                 parsed_prompt = json.loads(prompt)
#             except Exception as e:
#                 logger.error(f"Failed to parse prompt JSON: {str(e)}")
#                 raise HTTPException(status_code=400, detail="Invalid prompt JSON")

#         files_info = []
#         for file in files:
#             if not file.filename.lower().endswith(".pdf") or file.content_type != "application/pdf":
#                 logger.warning(f"Invalid file type: {file.filename}")
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"File '{file.filename}' is not a valid PDF"
#                 )
#             content = await file.read()
#             files_info.append({
#                 "filename": file.filename,
#                 "content_type": file.content_type,
#                 "size": len(content)
#             })
#             logger.info(f"Processed file: {file.filename}")

#         logger.info("Successfully processed all files, criteria, and prompt")
#         # Format the output for best readability
#         return {
#             "status": "success",
#             "message": f"{len(files)} PDF file(s), criteria, and job description received successfully",
#             "files": [
#                 {
#                     "filename": f["filename"],
#                     "content_type": f["content_type"],
#                     "size (bytes)": f["size"]
#                 } for f in files_info
#             ],
#             "criteria": [
#                 {
#                     "name": c.get("name"),
#                     "weight": c.get("weight"),
#                     "description": c.get("description")
#                 } for c in parsed_criteria
#             ],
#             "job_description": parsed_prompt["job_description"] if parsed_prompt and "job_description" in parsed_prompt else None
#         }
#     except Exception as e:
#         logger.error(f"Error in test-input endpoint: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# @app.post("/upload-preview")
# async def upload_preview(
#     files: List[UploadFile] = File(...),
# ):
#     """
#     This endpoint is used to upload a PDF file and return the metadata of the file.
#     """
#     try:
#         logger.info(f"Received upload-preview request with {len(files)} files")
#         if not files:
#             logger.warning("No files provided in request")
#             raise HTTPException(status_code=400, detail="No files provided")

#         files_info = []

#         for file in files:
#             # Validate file type by extension and content type
#             if not file.filename.lower().endswith(".pdf") or file.content_type != "application/pdf":
#                 logger.warning(f"Invalid file type: {file.filename}")
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"File '{file.filename}' is not a valid PDF"
#                 )

#             content = await file.read()
#             files_info.append({
#                 "filename": file.filename,
#                 "content_type": file.content_type,
#                 "size": len(content)
#             })
#             logger.info(f"Processed file: {file.filename}")

#         logger.info("Successfully processed all files")

#         return {
#             "status": "success",
#             "message": f"{len(files)} PDF file(s) received successfully",
#             "files": files_info
#         }

#     except Exception as e:
#         logger.error(f"Error in upload-preview endpoint: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
# @app.post("/process-cv")
# async def process_cv(file: UploadFile = File(...)):
#     try:
#         logger.info(f"Received CV processing request for file: {file.filename}")
        
#         # Initialize OCR service
#         ocr_service = OCRService()
        
#         # Process the document using OCR service
#         result = await ocr_service.parse_document(file)
        
#         logger.info(result)
#         return {
#             "status": "success",
#             "result": result
#         }
        
#     except Exception as e:
#         logger.error(f"Error processing CV: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

# @app.post("/rank-cvs")
# async def rank_cvs(
#     files: List[UploadFile] = File(...),
#     criteria: str = Form(...),
#     prompt: str = Form(None)
# ):
#     """
#     This endpoint receives a list of CVs (PDFs), criteria, and a job description,
#     processes them, and returns a ranked list of CVs based on how well they match the criteria.
#     """
#     try:
#         logger.info(f"Received rank-cvs request with {len(files)} files, criteria: {criteria}, and prompt: {prompt}")
        
#         if not files:
#             logger.warning("No files provided in request")
#             raise HTTPException(status_code=400, detail="No files provided")
#         if not criteria:
#             logger.warning("No criteria provided in request")
#             raise HTTPException(status_code=400, detail="No criteria provided")
#         if not prompt:
#             logger.warning("No prompt (job description) provided in request")
#             raise HTTPException(status_code=400, detail="No prompt (job description) provided")

#         # Parse criteria JSON
#         try:
#             parsed_criteria = json.loads(criteria)
#         except Exception as e:
#             logger.error(f"Failed to parse criteria JSON: {str(e)}")
#             raise HTTPException(status_code=400, detail="Invalid criteria JSON")

#         # Parse prompt JSON
#         parsed_prompt = None
#         if prompt:
#             try:
#                 parsed_prompt = json.loads(prompt)
#             except Exception as e:
#                 logger.error(f"Failed to parse prompt JSON: {str(e)}")
#                 raise HTTPException(status_code=400, detail="Invalid prompt JSON")

#         # Initialize OCR service
#         ocr_service = OCRService()

#         cv_summaries = []
#         for file in files:
#             if not file.filename.lower().endswith(".pdf") or file.content_type != "application/pdf":
#                 logger.warning(f"Invalid file type: {file.filename}")
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"File '{file.filename}' is not a valid PDF"
#                 )
                
#             parsed_content = await ocr_service.parse_document(file)
#             combined_markdown = parsed_content.get("markdown_content", "")
#             logger.info(f"Extracted Markdown for {file.filename}:\n{combined_markdown}")
            
#             summary = await ocr_service.summarize_content(
#                 combined_markdown, 
#                 parsed_criteria, 
#                 parsed_prompt["job_description"] if parsed_prompt else None
#             )
            
#             cv_summaries.append({
#                 "filename": file.filename,
#                 "summary": summary
#             })

#         # Rank the CVs based on their summaries
#         ranked_cvs = await ocr_service.rank_cvs(cv_summaries, parsed_criteria)

#         logger.info("Successfully ranked CVs")
#         return {
#             "status": "success",
#             "ranked_cvs": ranked_cvs
#         }

#     except Exception as e:
#         logger.error(f"Error in rank-cvs endpoint: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error ranking CVs: {str(e)}")

@app.post("/analyze-cvs")
async def analyze_cvs(
    files: List[UploadFile] = File(...),
    criteria: str = Form(...),
    prompt: str = Form(None)
):
    try:
        # Validation and parsing (same as before)
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        if not criteria:
            raise HTTPException(status_code=400, detail="No criteria provided")
        if not prompt:
            raise HTTPException(status_code=400, detail="No prompt (job description) provided")

        try:
            parsed_criteria = json.loads(criteria)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid criteria JSON")

        try:
            parsed_prompt = json.loads(prompt)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid prompt JSON")

        ocr_service = OCRService()
        cv_contents = []
        for file in files:
            if not file.filename.lower().endswith(".pdf") or file.content_type != "application/pdf":
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' is not a valid PDF"
                )
            parsed_content = await ocr_service.parse_document(file)
            combined_markdown = parsed_content.get("markdown_content", "")
            cv_contents.append({
                "filename": file.filename,
                "content": combined_markdown
            })

        results = await ocr_service.analyze_cvs(
            cv_contents,
            parsed_criteria,
            parsed_prompt["job_description"]
        )

        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing CVs: {str(e)}")

#@app.post("/convert-pdf-to-images")
#async def convert_pdf_to_images(file: UploadFile = File(...), dpi: int = 200):
#    """
#    Convert a PDF file to a list of images.
#    Each image is returned as a base64-encoded string.
#    """
#    try:
#        logger.info(f"Received PDF conversion request for file: {file.filename}")
        
#        # Validate file type
#        if not file.filename.lower().endswith(".pdf") or file.content_type != "application/pdf":
#            raise HTTPException(
#                status_code=400,
#                detail="File must be a PDF"
#            )
        
#        # Initialize PDF service
#        pdf_service = PDFService()
        
#        # Convert PDF to images
#        images = await pdf_service.convert_pdf_to_images(file, dpi)
        
#        logger.info(f"Successfully converted PDF to {len(images)} images")
#        return {
#            "status": "success",
#            "images": images
#        }
        
#    except Exception as e:
#        logger.error(f"Error converting PDF to images: {str(e)}")
#        raise HTTPException(status_code=500, detail=str(e))





