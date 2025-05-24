from models import Criterion
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy.exc import OperationalError
import os

logger = logging.getLogger(__name__)

# Replace with your actual database URL (e.g., SQLite for local dev or PostgreSQL in prod)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:dbpass@localhost:5432/ceveai")  # Use PostgreSQL URI in production

# Create engine with connection verification
try:
    logger.info("Attempting to connect to PostgreSQL database...")
    engine = create_engine(DATABASE_URL)
    # Test the connection
    with engine.connect() as connection:
        logger.info("Successfully connected to PostgreSQL database")
except OperationalError as e:
    logger.error(f"Failed to connect to PostgreSQL database: {str(e)}")
    logger.error("Please ensure PostgreSQL is installed and running")
    raise

# Session local for dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

def create_default_rows():
    """Create default rows in the database if they don't exist."""
    try:
        logger.info("Checking for default rows...")
        db = SessionLocal()
        
        default_criteria = [
            {
                "name": "Grammar",
                "description": "Assess the CV for correct grammar, punctuation, and spelling. Penalize for frequent errors, awkward phrasing, or lack of clarity. Reward concise and professionally structured language."
            },
            {
                "name": "Experience",
                "description": "Evaluate the candidate's work history in terms of relevance to the job description, duration of roles, progression, and specific responsibilities or achievements. Prioritize recent and high-impact experience."
            },
            {
                "name": "Education",
                "description": "Analyze the candidate's academic qualifications, including degrees, certifications, and institution prestige. Consider relevance to the job field and any continued learning or specialization."
            },
            {
                "name": "Skills",
                "description": "Examine the listed hard and soft skills. Determine how well they match the required skills in the job description. Highlight technical proficiencies, tools, frameworks, or domain-specific abilities."
            },
            {
                "name": "Leadership",
                "description": "Identify examples of leading teams, projects, or initiatives. Consider formal leadership roles (e.g., manager, team lead) and informal leadership (mentorship, initiative-taking). Emphasize scope and impact."
            },
            {
                "name": "Teamwork",
                "description": "Look for instances of collaboration in teams, cross-functional work, or contributions to group success. Note any roles that required interpersonal coordination, conflict resolution, or support of others."
            },
            {
                "name": "Relevance",
                "description": "Measure how well the candidate's overall profile — including experience, education, and skills — aligns with the job description. Emphasize alignment with specific responsibilities, industry domain, and required qualifications. Penalize unrelated or off-topic content."
            }
        ]
        
        for criterion_data in default_criteria:
            existing = db.query(Criterion).filter(Criterion.name == criterion_data["name"]).first()
            if not existing:
                logger.info(f"Creating default criterion: {criterion_data['name']}")
                new_criterion = Criterion(**criterion_data)
                db.add(new_criterion)
        
        db.commit()
        logger.info("Default rows check completed")
    except Exception as e:
        logger.error(f"Error creating default rows: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

