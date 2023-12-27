from pydantic import BaseModel


# Shared properties
class UserSchema(BaseModel):
    # Personal information
    email: str
    wallet_address: str


# Properties to receive via API on update
class UserCreate(BaseModel):
    email: str
    wallet_address: str
