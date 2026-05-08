from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import models
from schemas import schemas

router = APIRouter(
    tags=['guests']
)

# GET /
@router.get('/', response_model=List[schemas.BlogResponse], status_code=status.HTTP_200_OK)
async def read_blogs(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Blog).all()

# Get /blog_id
@router.get('/{blog_id}', response_model=schemas.BlogResponse, status_code=status.HTTP_200_OK)
async def read_blog(blog_id:int, db: Annotated[Session, Depends(get_db)]):
    blog = db.query(models.Blog).filter(models.Blog.blog_id == blog_id).first()

    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with id {blog_id} not found'
        )
    
    return blog