from datetime import datetime

from pydantic import BaseModel

class UserCreate(BaseModel):
    """ Schema for a new user, containing fields such as full_name, username and password """
    full_name: str
    username: str
    password: str

class Token(BaseModel):
    """ Schema for a Token, containing access_token and token_type """
    access_token: str
    token_type: str

class BlogCreate(BaseModel):
    """ Schema for a blog, containing fields like title and content """
    title: str
    content: str

class BlogResponse(BaseModel):
    """ Schema for a blog response """
    blog_id: int
    title: str
    content: str
    created_at: datetime

class BlogUpdate(BaseModel):
    """ Schema for a blog update """
    title: str | None = None
    content: str | None = None

