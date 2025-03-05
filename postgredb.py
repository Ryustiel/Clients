"""
Handles connecting to a postgre database that supports pgvector.

[tool.poetry.dependencies]
psycopg = {extras = ["binary", "async"], version = "^3.2.5"}
"""
from typing import (
    Any,
    Generator,
    Optional,
)

from sqlalchemy import create_engine, text, Engine, Result
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

# ==================================================== HANDLER

class SessionHandler:
    """
    Handles the session.
    """
    def __init__(self, session_maker: sessionmaker, async_session_maker: async_sessionmaker):
        self._session_maker = session_maker
        self._async_session_maker = async_session_maker
        self._session = None
        self._async_session = None

    @property
    def session(self) -> Session:
        if self._session is None:
            self._session = self._session_maker()
        return self._session
    
    @property
    def async_session(self) -> AsyncSession:
        if self._async_session is None:
            self._async_session = self._async_session_maker()
        return self._async_session

    def __enter__(self) -> Session:
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
    
    async def __aenter__(self) -> Session:
        return self.async_session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.async_session.rollback()
        else:
            await self.async_session.commit()
        await self.async_session.close()

# ======================================================= CLIENT

class PostgreDatabaseClient:
    """
    A simple client using SQLAlchemy to interact with a postgre database.
    """
    def __init__(self, connection_string: str):

        self.engine = create_engine(connection_string)
        self.sessionmaker = sessionmaker(bind=self.engine)

        self.async_engine = create_async_engine(connection_string)
        self.async_sessionmarker = async_sessionmaker(bind=self.engine)

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
        """Makes sure the PGVector extension is active on the postgresql database."""
        with self.handler() as session:
            session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

    # ================================================================= QUERY OPERATIONS

    def query(self, query: str) -> Result:
        """
        Runs the query on the database and returns the result as a sqlalchemy object.
        """
        with self.handler() as session:
            return session.execute(text(query))
        
    async def aquery(self, query: str) -> Result:
        """
        Runs the query on the database and returns the result as a sqlalchemy object.
        """
        async with self.handler() as session:
            return await session.execute(text(query))

    # ================================================================= SESSION HANDLING

    def session(self) -> Session:
        return self.sessionmaker()
    
    def asession(self) -> AsyncSession:
        return self.async_sessionmarker()

    def handler(self) -> SessionHandler:
        """
        Create a SessionHandler, 
        which supports both synchronous and asynchronous sessions. 
        Use the context manager (with / async with) to create a session.
        """
        return SessionHandler(session_maker=self.sessionmaker, async_session_maker=self.async_sessionmarker)

    def __call__(self) -> SessionHandler:
        """
        Create a SessionHandler, 
        exposing a Session when used in a context manager.
        """
        return self.handler()
    