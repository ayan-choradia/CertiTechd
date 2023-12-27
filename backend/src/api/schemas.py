from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    UserSchema representing details of login form for authentication.

    Attributes:
    ----------------
    username: str
        The username of the user.
    password: str
        The password of the user.
    """

    wallet_address: str
    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """
    UserCreate representing details of signup form for authentication.

    Attributes:
    ----------------
    username: str
        The username of the user.
    password: str
        The password of the user.
    """

    user_name: str
    wallet_address: str

    class Config:
        orm_mode = True


class CreateCertSchema(BaseModel):
    recipent_address: str
    data: str
    manufacturing_date: int
    expiry_date: int
