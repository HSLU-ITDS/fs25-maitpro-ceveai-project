import os
import logging
from datetime import datetime
import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, Form, File, Depends, Request
from typing import List, Annotated
from fastapi.middleware.cors import CORSMiddleware
from services.llm_service import get_llm_service
from services.ocr_services import OCRService
from pydantic import BaseModel
from database import engine, SessionLocal, create_default_rows
from sqlalchemy.orm import Session
from models import Base, Criterion, JobAnalysis, CVAnalysis, CVScore, JobAnalysisCriterion
from schemas import CriterionCreate, CriterionOut
from fastapi.responses import StreamingResponse
from services.generatePDF import create_candidates_pdf
import traceback

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

Base.metadata.create_all(bind=engine)
create_default_rows()
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
        job_analysis = JobAnalysis(prompt=parsed_prompt["job_description"])
        db.add(job_analysis)
        db.flush()

        # Create JobAnalysisCriterion records
        job_analysis_criteria_map = {
            c["id"]: JobAnalysisCriterion(
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
            cv_analysis = CVAnalysis(
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
                    scores.append(CVScore(
                        cv_analysis_id=cv_analysis.id,
                        job_analysis_criterion_id=job_analysis_criteria_map[criterion["id"]].id,
                        score=round(float(score_data["score"]), 1),
                        explanation=score_data.get("explanation", "")
                    ))
            db.add_all(scores)

            # Format result for response
            formatted_results.append({
                "filename": result["filename"],
                "candidate": result.get("candidate", "Unknown"),
                "summary": result.get("summary", ""),
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
        criterion = db.query(Criterion).filter(Criterion.id == criterion_id).first()
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
            db.query(CVAnalysis)
            .filter(CVAnalysis.job_analysis_id == job_analysis_id)
            .order_by(CVAnalysis.total_score.desc())
            .all()
        )
        candidates = []
        for idx, cv in enumerate(cv_analyses):
            # Fetch all CVScore for this CVAnalysis
            scores = db.query(CVScore).filter(CVScore.cv_analysis_id == cv.id).all()
            # For each score, get the criterion name
            score_list = []
            for score in scores:
                # Join to get criterion name
                job_analysis_criterion = db.query(JobAnalysisCriterion).filter(JobAnalysisCriterion.id == score.job_analysis_criterion_id).first()
                criterion = db.query(Criterion).filter(Criterion.id == job_analysis_criterion.criterion_id).first() if job_analysis_criterion else None
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
        criteria = db.query(Criterion).all()
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
    existing = db.query(Criterion).filter(Criterion.name == criterion.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Criterion with this name already exists.")
    new_criterion = Criterion(name=criterion.name, description=criterion.description)
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

@app.get("/job-analyses")
async def get_job_analyses(db: Session = Depends(get_db)):
    try:
        # Fetch all job analyses ordered by creation date (newest first)
        job_analyses = (
            db.query(JobAnalysis)
            .order_by(JobAnalysis.created_at.desc())
            .all()
        )
        
        return {
            "status": "success",
            "job_analyses": [
                {
                    "id": str(analysis.id),  # Convert UUID to string
                    "created_at": analysis.created_at.isoformat()
                } for analysis in job_analyses
            ]
        }
    except Exception as e:
        logger.error(f"Error retrieving job analyses: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))