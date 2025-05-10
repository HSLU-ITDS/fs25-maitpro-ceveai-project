# schemas.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CriterionCreate(BaseModel):
    name: str
    description: str

class CriterionOut(BaseModel):
    id: int
    name: str
    description: str
    class Config:
        orm_mode = True

class JobAnalysisCriterionCreate(BaseModel):
    criterion_id: int
    weight: float

class JobAnalysisCreate(BaseModel):
    prompt: str
    criteria: List[JobAnalysisCriterionCreate]

class JobAnalysisOut(BaseModel):
    id: int
    prompt: str
    created_at: datetime
    class Config:
        orm_mode = True

class CVScoreCreate(BaseModel):
    job_analysis_criterion_id: int
    score: float
    explanation: Optional[str]

class CVScoreOut(BaseModel):
    job_analysis_criterion_id: int
    score: float
    explanation: Optional[str]
    class Config:
        orm_mode = True

class CVAnalysisCreate(BaseModel):
    job_analysis_id: int
    filename: str
    candidate_name: str
    summary: Optional[str]
    total_score: Optional[float]
    scores: List[CVScoreCreate]

class CVAnalysisOut(BaseModel):
    id: int
    filename: str
    candidate_name: str
    summary: Optional[str]
    total_score: Optional[float]
    scores: List[CVScoreOut]
    class Config:
        orm_mode = True