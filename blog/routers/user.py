from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, oauth2
from ..repo.user import UserRepo
from ..database import get_db

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return UserRepo.create_user(request, db)

@router.get('', response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return UserRepo.get_all_user(db)

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = UserRepo.get_user(id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detaile=f'User with {id} not found')
    return user