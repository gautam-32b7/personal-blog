from typing import Annotated, List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models import models
from schemas import schemas
from database import get_db
from routers import users

router = APIRouter(
    tags=['blogs']
)

# reusable dependency that injects the current user as a dict using get_current_user
user_dep = Annotated[dict, Depends(users.get_current_user)]

# GET /blogs
@router.get('/blogs', response_model=List[schemas.BlogResponse], status_code=status.HTTP_200_OK)
async def read_articles(db: Annotated[Session, Depends(get_db)], user: user_dep):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    return db.query(models.Blog).filter(models.Blog.user_id == user.get('id')).all()

# GET /blogs/blog_id
@router.get('/blogs/{blog_id}', response_model=schemas.BlogResponse, status_code=status.HTTP_200_OK)
async def read_blog(blog_id: int, db: Annotated[Session, Depends(get_db)], user: user_dep):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    blog = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).filter(models.Blog.user_id == user.get('id')).first()
    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Blog not found'
        )
    
    return blog

# POST /blogs
@router.post('/blogs', response_model=schemas.BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: schemas.BlogCreate, db: Annotated[Session, Depends(get_db)], user: user_dep):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    new_blog = models.Blog(
        title=blog.title,
        content=blog.content,
        user_id=user.get('id')
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog 

# PUT /blogs/blog_id
@router.put('/blogs/{blog_id}', response_model=schemas.BlogResponse, status_code=status.HTTP_200_OK)
async def update_blog(blog_id: int, update_blog: schemas.BlogUpdate, db: Annotated[Session, Depends(get_db)], user: user_dep):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    blog = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).filter(models.Blog.user_id == user.get('id')).first()

    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with id {blog_id} not found'
        )
    
    if update_blog.title:
        blog.title = update_blog.title
    
    if update_blog.content:
        blog.content = update_blog.content
    
    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog

# DELETE /blogs/blog_id
@router.delete('/blogs/blog_id', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id: int, db: Annotated[Session, Depends(get_db)], user: user_dep):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    blog = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).filter(models.Blog.user_id == user.get('id')).first()

    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with id {blog_id} not found'
        )
    db.query(models.Blog).filter(models.Blog.blog_id == blog_id).filter(models.Blog.user_id == user.get('id')).delete()
    db.commit()