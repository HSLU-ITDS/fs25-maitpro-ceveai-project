from sqlalchemy import Column, String, Text, Float, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, UTC
import uuid

Base = declarative_base()

class Criterion(Base):
    __tablename__ = 'criteria'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    job_analysis_criteria = relationship("JobAnalysisCriterion", back_populates="criterion", cascade="all, delete-orphan")


class JobAnalysis(Base):
    __tablename__ = 'job_analyses'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    prompt = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    criteria = relationship("JobAnalysisCriterion", back_populates="job_analysis", cascade="all, delete-orphan")
    cv_analyses = relationship("CVAnalysis", back_populates="job_analysis", cascade="all, delete-orphan")


class JobAnalysisCriterion(Base):
    __tablename__ = 'job_analysis_criteria'
    id = Column(Integer, primary_key=True, index=True)
    job_analysis_id = Column(UUID(as_uuid=True), ForeignKey('job_analyses.id'))
    criterion_id = Column(Integer, ForeignKey('criteria.id'))
    weight = Column(Float, nullable=False)
    job_analysis = relationship("JobAnalysis", back_populates="criteria")
    criterion = relationship("Criterion", back_populates="job_analysis_criteria")
    cv_scores = relationship("CVScore", back_populates="job_analysis_criterion", cascade="all, delete-orphan")


class CVAnalysis(Base):
    __tablename__ = 'cv_analyses'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    job_analysis_id = Column(UUID(as_uuid=True), ForeignKey('job_analyses.id'))
    filename = Column(String, nullable=False)
    candidate_name = Column(String, nullable=False)
    summary = Column(Text)
    total_score = Column(Float)
    job_analysis = relationship("JobAnalysis", back_populates="cv_analyses")
    scores = relationship("CVScore", back_populates="cv_analysis", cascade="all, delete-orphan")


class CVScore(Base):
    __tablename__ = 'cv_scores'
    id = Column(Integer, primary_key=True, index=True)
    cv_analysis_id = Column(UUID(as_uuid=True), ForeignKey('cv_analyses.id'))
    job_analysis_criterion_id = Column(Integer, ForeignKey('job_analysis_criteria.id'))
    score = Column(Float, nullable=False)
    explanation = Column(Text)
    cv_analysis = relationship("CVAnalysis", back_populates="scores")
    job_analysis_criterion = relationship("JobAnalysisCriterion", back_populates="cv_scores")
