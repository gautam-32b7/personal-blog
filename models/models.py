from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from database import Base

class User(Base):
    """ SQLAlchemy model representing a user in the system """

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

class Blog(Base):
    """ SQLAlchemy model representing a blog in the system """

    __tablename__ = 'blogs'

    blog_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    user_id = Column(Integer, ForeignKey('users.user_id'))

