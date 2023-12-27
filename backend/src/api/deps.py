from web3 import Web3

from src.abi import CERT_ABI

web3 = Web3(
    Web3.HTTPProvider(
        "https://polygon-mainnet.infura.io/v3/c5cd1475b289436892d89a9756f2be63"
    )
)


contract = web3.eth.contract(
    address=web3.to_checksum_address("0x55f60e1f70af9f2c6f8e71335872ecf5610e5d65"),
    abi=CERT_ABI,
)


def sign_transaction(transaction, private_key):
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    return transaction_hash.hex()
