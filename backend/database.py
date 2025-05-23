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

# Base class for models to inherit from
Base = declarative_base()

def create_tables():
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

