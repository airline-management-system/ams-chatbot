from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
from langchain_community.utilities import SQLDatabase


class PostgreDB:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()
        self.connect()
    
    def connect(self) -> None:
        """Establish database connection"""
        try:
            DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/ams-local"
            self.engine = create_engine(DATABASE_URL)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {str(e)}")
    
    def get_session(self):
        """Get a new database session"""
        if not self.SessionLocal:
            self.connect()
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    def get_langchain_type_connection(self):
        return SQLDatabase(engine=self.engine)
    
    def close(self) -> None:
        """Close the database connection"""
        if self.engine:
            self.engine.dispose()
    
    def __del__(self):
        """Cleanup when the object is destroyed"""
        self.close()