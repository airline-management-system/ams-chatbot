from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
from langchain_community.utilities import SQLDatabase
from application.config import Config


class PostgreDB:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()
        self.connect()
    
    def connect(self) -> None:
        """Establish database connection"""
        try:
            db_config = Config.get_database_config()
            DATABASE_URL = f"postgresql://{db_config['type']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
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