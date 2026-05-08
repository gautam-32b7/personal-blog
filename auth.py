from datetime import datetime, timedelta, UTC

from pwdlib import PasswordHash
from jose import JWTError, jwt

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """ Takes a plain-text password and return its hashed version"""
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Compares plain-text password with hashed password and return True if they match """
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """ Creates a JWT access token by copying the input data + adding expiration time """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    """ Decodes JWT token """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        return None