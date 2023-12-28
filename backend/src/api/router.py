from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.deps import contract, web3
from src.api.schemas import CreateCertSchema, CreateUser
from src.db.session import get_db_session
from src.user.models import User
from src.user.router import router as user_router
from src.user.utils import get_current_user

router = APIRouter()
# Adds configuration to all router files.
router.include_router(user_router, prefix="/users", tags=["users"])


@router.get("/health/")
async def health():
    """
    Used to check the health of the API and if it is running successfully on the server.
    """
    return "Ok"


@router.get("/setcount/")
async def set_temp_count(
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    transaction_ = contract.functions.setTempCount().build_transaction(
        {
            "chainId": 137,
            "gas": 500000,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(
                web3.to_checksum_address(user["wallet_address"])
            ),
        }
    )
    return transaction_


@router.get("/getcount/")
async def get_temp_count(
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    count = contract.functions.getTempCount().call()
    return count


@router.get("/create-cert/")
async def create_certificate(
    data=CreateCertSchema,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    transaction_ = contract.functions.createCertificate(
        data.recipent_address, data.data, data.manufacturing_date, data.expiry_date
    ).build_transaction(
        {
            "chainId": 137,
            "gas": 500000,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(
                web3.to_checksum_address(user["wallet_address"])
            ),
        }
    )
    return transaction_


@router.post("/create-user/")
async def createUser(
    data:CreateUser,
    db: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):

    current_user = db.query(User).filter(User.wallet_address == user["wallet_address"]).first()
    print(current_user.role)
    stoed_user = db.query(User).where(User.wallet_address == data.wallet_address).first()
    if stoed_user:
        raise HTTPException(status_code=401, detail="Aready Exist")
    if current_user.role == "industry":
        transaction_ = contract.functions.updateRole(
            web3.to_checksum_address(data.wallet_address), "broker"
        ).build_transaction(
            {
                "chainId": 137,
                "gas": 500000,
                "gasPrice": web3.eth.gas_price,
                "nonce": web3.eth.get_transaction_count(
                    web3.to_checksum_address(user["wallet_address"])
                ),
            }
        )
        stoed_user = db.query(User).where(User.wallet_address == data.wallet_address).first()
        if not stoed_user:
            user  = User(wallet_address=data.wallet_address, role='broker')
    elif current_user.role == "broker":
        transaction_ = contract.functions.updateRole(
            web3.to_checksum_address(data.wallet_address), "client"
        ).build_transaction(
            {
                "chainId": 137,
                "gas": 500000,
                "gasPrice": web3.eth.gas_price,
                "nonce": web3.eth.get_transaction_count(
                    web3.to_checksum_address(user["wallet_address"])
                ),
            }
        )
        stoed_user = db.query(User).where(User.wallet_address == data.wallet_address).first()
        if not stoed_user:
            user  = User(wallet_address=data.wallet_address, role='client')
    else:
        raise HTTPException(status_code=401, detail="No Rights for this function")
    db.add(user)
    db.commit()
    return transaction_
