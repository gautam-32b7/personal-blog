from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from schemas import schemas
from models import models
from auth import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter(
    tags=['users']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """ Get current user from toekn """
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Could not validate credentials', 
            headers={'WWW-Authenticate': 'Bearer'}
            )
    
    user_id = payload.get('id')
    username = payload.get('sub')

    if not user_id or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Could not validate credentials', 
            headers={'WWW-Authenticate': 'Bearer'}
            )
    
    return {'id': user_id, 'username': username}

# POST /register
@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    # check if username already exist
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='username already registered')
    
    hashed_pw = hash_password(user.password)

    new_user = models.User(
        full_name=user.full_name,
        username=user.username,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# POST /login
@router.post('/login', response_model=schemas.Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect username or password', headers={'WWW-Authenticate': 'Bearer'})
    
    access_token = create_access_token(data={'sub': user.username, 'id': user.user_id})
    return {'access_token': access_token, 'token_type': 'bearer'}