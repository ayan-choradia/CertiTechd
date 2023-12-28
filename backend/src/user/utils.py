import logging
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext

from src.api.schemas import UserSchema
from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoggingHTTPBearer(HTTPBearer):
    """
    Custom HTTPBearer class that logs the Authorization header and the credentials.

    Methods:
    ------------
    __call__: Overrides the __call__ method of the parent class.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the LoggingHTTPBearer class.
        """
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        """
        Overrides the __call__ method of the parent class.
        """
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            self.logger.info("Missing Authorization header.")

        scheme, credentials = get_authorization_scheme_param(authorization)

        if not scheme or not credentials:
            self.logger.info(
                f"Scheme or credentials missing. Scheme: {scheme}, Credentials: {credentials}"
            )

        if scheme.lower() != "bearer":
            self.logger.info(f"Invalid scheme. Expected 'bearer', got {scheme.lower()}")

        try:
            return await super().__call__(request)
        except HTTPException as e:
            self.logger.info(f"HTTPException raised: {e}")
            raise e


oauth2_bearer = LoggingHTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_bearer),
) -> UserSchema:
    """
    Funtion that returns the current user.

    Attributes:
    ----------------
    token: The token of the current user.

    Returns:
    ----------------
    UserSchema: The current user.
    """
    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        wallet_address = payload.get("sub")
        role = payload.get("sub")
        id = payload.get("id")
        if wallet_address is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return {"wallet_address": wallet_address, "id": id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Function that creates an access token.

    Attributes:
    ----------------
    data: The data to be encoded in the token.
    expires_delta: The expiration time of the token.

    Returns:
    ----------------
    str: The encoded token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
