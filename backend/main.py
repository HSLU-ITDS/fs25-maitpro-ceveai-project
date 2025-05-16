import os
import logging
from datetime import datetime
import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, Form, File, Depends, Request
from typing import List, Annotated
from fastapi.middleware.cors import CORSMiddleware
from .services.llm_service import get_llm_service
from .services.ocr_services import OCRService
from pydantic import BaseModel
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from . import models
from backend.schemas import CriterionCreate, CriterionOut
from fastapi.responses import StreamingResponse
from .services.generatePDF import create_candidates_pdf
#from services.pdf_service import PDFService

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

models.Base.metadata.create_all(bind=engine)
logger.info("Created db tables")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
logger.info("CORS middleware configured")

def get_db():
    logger.info("Creating new database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.info("Closing database session")
        db.close()

def to_pascal_case(name: str) -> str:
    """
    Convert a string to Pascal case, handling all types of input casing.
    Examples: 
    - "john doe" -> "John Doe"
    - "JOHN DOE" -> "John Doe"
    - "jOhN dOe" -> "John Doe"
    - "John Doe" -> "John Doe"
    """
    if not name or name == "N/A":
        return name
    return " ".join(word.capitalize() for word in name.lower().split())

db_dependency = Annotated[Session, Depends(get_db)]

def compute_weighted_total(scores, parsed_criteria):
    """
    Compute the weighted total score (0-10 scale) given a dictionary of scores and the criteria with weights.
    """
    if not scores or not parsed_criteria:
        return 0.0
        
    # Create a mapping of criterion names to weights
    name_to_weight = {c["name"]: float(c["weight"]) for c in parsed_criteria}
    
    # Calculate weighted sum and total weight in one pass
    weighted_sum = sum(
        float(score_data["score"]) * name_to_weight.get(criterion_name, 0.0)
        for criterion_name, score_data in scores.items()
    )
    total_weight = sum(name_to_weight.get(name, 0.0) for name in scores.keys())
    
    # Calculate final score
    total_score = weighted_sum / total_weight if total_weight > 0 else 0.0
    return min(round(total_score, 1), 10.0)

@app.post("/analyze-cvs")
async def analyze_cvs(
    files: List[UploadFile] = File(...),
    criteria: str = Form(...),
    prompt: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # Parse and validate input
        parsed_criteria = json.loads(criteria)
        parsed_prompt = json.loads(prompt)
        logger.info(f"Processing {len(files)} files with {len(parsed_criteria)} criteria")

        # Create JobAnalysis
        job_analysis = models.JobAnalysis(prompt=parsed_prompt["job_description"])
        db.add(job_analysis)
        db.flush()

        # Create JobAnalysisCriterion records
        job_analysis_criteria_map = {
            c["id"]: models.JobAnalysisCriterion(
                job_analysis_id=job_analysis.id,
                criterion_id=c["id"],
                weight=c["weight"]
            )
            for c in parsed_criteria
        }
        db.add_all(job_analysis_criteria_map.values())
        db.flush()

        # Process CVs
        ocr_service = OCRService()
        cv_contents = []
        for file in files:
            parsed_content = await ocr_service.parse_document(file)
            cv_contents.append({
                "filename": file.filename,
                "content": parsed_content.get("markdown_content", "")
            })

        # Get results from OCR service
        results = await ocr_service.analyze_cvs(
            cv_contents,
            parsed_criteria,
            parsed_prompt["job_description"]
        )

        # Process and save results
        formatted_results = []
        for result in results:
            # Create CVAnalysis
            cv_analysis = models.CVAnalysis(
                job_analysis_id=job_analysis.id,
                filename=result["filename"],
                candidate_name=to_pascal_case(result.get("candidate", "Unknown")),
                summary=result.get("summary", ""),
                total_score=compute_weighted_total(result.get("scores", {}), parsed_criteria)
            )
            db.add(cv_analysis)
            db.flush()

            # Create CVScores
            scores = []
            for criterion in parsed_criteria:
                score_data = result["scores"].get(criterion["name"], {})
                if score_data:
                    scores.append(models.CVScore(
                        cv_analysis_id=cv_analysis.id,
                        job_analysis_criterion_id=job_analysis_criteria_map[criterion["id"]].id,
                        score=round(float(score_data["score"]), 1),
                        explanation=score_data.get("explanation", "")
                    ))
            db.add_all(scores)

            # Format result for response
            formatted_results.append({
                "filename": result["filename"],
                "candidate": result["candidate"],
                "summary": result["summary"],
                "scores": [
                    {
                        "criterion_name": criterion["name"],
                        "score": round(float(result["scores"][criterion["name"]]["score"]), 1),
                        "explanation": result["scores"][criterion["name"]].get("explanation", "")
                    }
                    for criterion in parsed_criteria
                    if criterion["name"] in result["scores"]
                ]
            })

        db.commit()
        return {
            "status": "success",
            "results": formatted_results,
            "job_analysis_id": str(job_analysis.id)
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Error analyzing CVs: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error analyzing CVs: {str(e)}")

@app.get("/criteria/{criterion_id}")
async def get_criterion(criterion_id: int, db: Session = Depends(get_db)):
    try:
        criterion = db.query(models.Criterion).filter(models.Criterion.id == criterion_id).first()
        if not criterion:
            raise HTTPException(status_code=404, detail=f"Criterion with id {criterion_id} not found")
        return criterion
    except Exception as e:
        logger.error(f"Error retrieving criterion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{job_analysis_id}")
async def get_results(job_analysis_id: str, db: Session = Depends(get_db)):
    try:
        # Fetch all CVAnalysis for this job_analysis_id, ordered by total_score descending
        cv_analyses = (
            db.query(models.CVAnalysis)
            .filter(models.CVAnalysis.job_analysis_id == job_analysis_id)
            .order_by(models.CVAnalysis.total_score.desc())
            .all()
        )
        candidates = []
        for idx, cv in enumerate(cv_analyses):
            # Fetch all CVScore for this CVAnalysis
            scores = db.query(models.CVScore).filter(models.CVScore.cv_analysis_id == cv.id).all()
            # For each score, get the criterion name
            score_list = []
            for score in scores:
                # Join to get criterion name
                job_analysis_criterion = db.query(models.JobAnalysisCriterion).filter(models.JobAnalysisCriterion.id == score.job_analysis_criterion_id).first()
                criterion = db.query(models.Criterion).filter(models.Criterion.id == job_analysis_criterion.criterion_id).first() if job_analysis_criterion else None
                score_list.append({
                    "criterion": criterion.name if criterion else "Unknown",
                    "score": round(score.score, 1),
                    "explanation": score.explanation if score.explanation else ""
                })
            candidates.append({
                "index": idx + 1,  # 1-based index for rank
                "filename": cv.filename,
                "candidate_name": cv.candidate_name,
                "summary": cv.summary,
                "total_score": round(cv.total_score, 1) if cv.total_score is not None else None,
                "scores": score_list
            })
        return {"candidates": candidates}
    except Exception as e:
        logger.error(f"Error retrieving results: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving results: {str(e)}")

@app.get("/criteria")
async def get_all_criteria(db: Session = Depends(get_db)):
    try:
        criteria = db.query(models.Criterion).all()
        return {
            "status": "success",
            "criteria": [
                {
                    "id": c.id,
                    "name": c.name,
                    "description": c.description
                } for c in criteria
            ]
        }
    except Exception as e:
        logger.error(f"Error retrieving criteria: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/criteria", response_model=CriterionOut)
async def create_criterion(criterion: CriterionCreate, db: Session = Depends(get_db)):
    # Check for duplicate name
    existing = db.query(models.Criterion).filter(models.Criterion.name == criterion.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Criterion with this name already exists.")
    new_criterion = models.Criterion(name=criterion.name, description=criterion.description)
    db.add(new_criterion)
    db.commit()
    db.refresh(new_criterion)
    return new_criterion

@app.post("/generate-pdf")
async def generate_pdf(request: Request):
    data = await request.json()
    candidates = data.get("candidates", [])
    print("Received candidates data:", candidates)

    # Generate PDF
    pdf_buffer = create_candidates_pdf(candidates)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report.pdf"}
    )

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





