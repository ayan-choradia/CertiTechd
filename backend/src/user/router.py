from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.deps import contract
from src.api.schemas import UserCreate
from src.config import settings
from src.db.session import get_db_session
from src.user.models import User
from src.user.utils import create_access_token, get_current_user

router = APIRouter()


@router.post("/auth")
async def signup(user: UserCreate, db: Session = Depends(get_db_session)):
    """
    Create a new user in the database and return a message if successful or raise an exception if the wallet_address already exists in the database.

    Arguments:
    ---------------
    user: UserCreate
        The user to be created in the database.
    db: AsyncSession = Depends(db_session)
        The database session.

    Returns:
    --------------
    dict: A dictionary containing a message if the user was created successfully.

    """
    existing_user = db.execute(
        select(User).where(User.wallet_address == user.wallet_address)
    )
    if existing_user.scalar():
        stored_user = db.execute(
            select(User).where(User.wallet_address == user.wallet_address)
        )
        stored_user = stored_user.scalar()
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": stored_user.wallet_address, "id": stored_user.id},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    role = contract.functions.hasRole(user.wallet_address).call()
    print(role)
    new_user = User(wallet_address=user.wallet_address, role=role)
    db.add(new_user)
    db.commit()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.wallet_address, "id": new_user.id},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/me")
async def read_user(
    db: Session = Depends(get_db_session), user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.wallet_address == user["wallet_address"]).first()
    return user
