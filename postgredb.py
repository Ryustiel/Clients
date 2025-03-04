"""
Handles connecting to a postgre database that supports pgvector.
"""
from typing import (
    Any,
    Generator,
    Optional,
)

from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

class SessionHandler:
    """
    Handles the session.
    """
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self) -> Session:
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.commit()
        self.session.close()
        return False  # Handle exceptions if necessary; return True to suppress them, False to propagate

class PostgreDatabaseClient:
    """
    A simple client using SQLAlchemy to interact with a postgre database.
    """
    def __init__(self, url: str):

        self.url = url
        self.engine = create_engine(self.url)
        self.sessionmaker = sessionmaker(bind=self.engine)

        self._active_context_session = None
    
    # ================================================================= MAINTAINANCE OPERATIONS
    
    def create_tables(self, base: DeclarativeBase):
        """Creates all tables in the database."""
        self.activate_pgvector()
        base.metadata.create_all(self.engine)

    def drop_tables(self):
        """Drops all tables in the database."""
        with self.handler() as session:
            session.execute(text("DROP SCHEMA public CASCADE"))
            session.execute(text("CREATE SCHEMA public"))

    def activate_pgvector(self):
        with self.handler() as session:
            session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

    # ================================================================= QUERY OPERATIONS



    # ================================================================= SESSION HANDLING

    def session(self) -> Session:
        return self.sessionmaker()

    def handler(self) -> SessionHandler:
        """
        Create a SessionHandler, 
        exposing a Session when used in a context manager.
        """
        return SessionHandler(session=self.session())

    def __call__(self) -> SessionHandler:
        """
        Create a SessionHandler, 
        exposing a Session when used in a context manager.
        """
        return self.handler()
    