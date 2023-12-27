import pathlib
from decimal import Decimal
import pyodbc
from sqlalchemy import create_engine

import yaml
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.config import settings
from src.cryptocurrency.models import Cryptocurrency
from src.cryptocurrency.services import (
    get_cryptocurrency_by_address_and_network,
    get_cryptocurrency_by_symbol_and_network,
)
from src.currency.services import get_or_create_currency
from src.db.base import Base
from src.network.models import Network
from src.network.services import (
    get_by_chain_id,
    get_or_create_network,
    update_network_from_dict,
)
from psycopg2 import sql



class CryptocurrencySchema(BaseModel):
    """
    Class that stores schema and data regarding to a certain cryptocurrency and uses the Pydantic Model. 

    More on the Pydantic Base Model: https://docs.pydantic.dev/usage/models/

    ...

    Attributes:
    -------------
    decimals: int
        Number of decimals that the cryptocurrency is divided to.
    address: str
        The contract address of the cryptocurrency in question.
    name: str 
        The name of the cryptocurrency.
    symbol: str
        The symbol of the cryptocurrency (i.e BTC, ETH)
    terra_denom: str
        If the cryptocurrency is a Terra native token, this holds the denom of the token as inscribed in the blockchain (i.e uluna)
    """

    decimals: int | None = None
    address: str | None = None
    name: str | None = None
    symbol: str | None = None
    terra_denom: str | None = None


class Currency(BaseModel):
    """
    Pydantic Model that stores schema and data regarding to a certain currency and uses the Pydantic model.

    More on the Pydantic Base Model: https://docs.pydantic.dev/usage/models/

    ...

    Attributes:
    -------------
    name: str
        The name of the currency
    code: str
        ISO currency code which represents a three-letter alphabetic code that represents the various currencies around the world. 

    """

    name: str | None = None
    code: str | None = None


class NetworkSchema(BaseModel):
    """
    Pydantic Model that stores the schema and data regarding a certain blockchain network and uses the Pydantic model.

    More on the Pydantic Base Model: https://docs.pydantic.dev/usage/models/

    ...

    Attributes:
    -------------
    chain_id: str | None
        Unique identifier that represents the blockchain network connected to (i.e Ethereum Chain ID is `1`, Juno Chain ID is `uni-5`)
    name: str | None
        Name of the Blockchain network
    node_url: str | None
        The URL of the node being used to access the blockchain network API
    type: str | None
        REVIEW
    native_token: str | None
        The native token of the blockchain which is used for transaction fees.
    native_token_decimals: str | None
        The decimals used for the native token.
    gas_limit: Decimal | None
        Maximum gas set by the node connected to. 
    confirmation_blocks: int | None
        The number of confirmations needed for a transaction to be accepted by the network. 
    max_filter_length: int | None
        REVIEW
    eumlet_contract_address: str | None
        the contract address of the Eumlet contract on the network.
    utils_contract_address: str | None
        the contract address of the Utils contract on the network.
    speed_up_gas_price_multiplier: float | None
        REVIEW
    cryptocurrencies: list[CryptocurrencySchema] | None
        A list of CryptocurrencySchema objects that exist on the blockchain
    """ 
    chain_id: str | None = None
    name: str | None = None
    node_url: str | None = None
    type: str | None = None
    native_token: str | None = None
    native_token_decimals: str | None = None
    gas_limit: Decimal | None = None
    confirmation_blocks: int | None = None
    max_filter_length: int | None = None
    eumlet_contract_address: str | None = None
    utils_contract_address: str | None = None
    speed_up_gas_price_multiplier: float | None = None
    cryptocurrencies: list[CryptocurrencySchema] | None = None


class Data(BaseModel):
    """
    Pydantic Model that stores a list of networks (NetworkSchema objects) and a list of currencies (Currency objects) and uses the Pydantic model.

    More on the Pydantic Base Model: https://docs.pydantic.dev/usage/models/

    ...

    Attributes:
    -------------
    networks: list[NetworkSchema]
        A list of networks and all their data using the NetworkSchema object.
    currencies: list[Currency]
        A list of currenices and all their data using the CurrencySchema object.

    """
    networks: list[NetworkSchema]
    currencies: list[Currency]


def init_data(db: Session, data: dict) -> None:
    """
    Initializes a db Session from a dictionary with network and curency data.

    ...

    Parameters:
    ------------
    db: Session
        A Session (read more about SQLAlchemy sessions: https://docs.sqlalchemy.org/en/20/orm/session_basics.html) that 
        connects to a database instance and allows read/write operations.

    data: dict
        A dictionary that holds two keys: networks and currencies
    
    

    """
    data: Data = Data(**data)

    for currency in data.currencies:
        currency = get_or_create_currency(db=db, obj_in=currency.dict())

    for network in data.networks:
        # Queries the database to check if the network exists in the database, if not it creates a Network object instance. 
        network_obj = (
            db.query(Network).where(Network.chain_id == network.chain_id).first()
        )
        if not network_obj:
            network_obj = Network()

        network_obj.chain_id = network.chain_id
        network_obj.node_url = network.node_url
        network_obj.name = network.name
        network_obj.type = network.type
        network_obj.native_token = network.native_token
        network_obj.native_token_decimals = network.native_token_decimals
        network_obj.eumlet_contract_address = network.eumlet_contract_address
        network_obj.utils_contract_address = network.utils_contract_address
        network_obj.gas_limit = network.gas_limit
        network_obj.confirmation_blocks = network.confirmation_blocks
        network_obj.max_filter_length = network.max_filter_length
        network_obj.speed_up_gas_price_multiplier = (
            network.speed_up_gas_price_multiplier
        )

        # It then commits the network object to the database. 
        db.add(network_obj)
        db.commit()
        for token in network.cryptocurrencies:
            # Same for cryptocurrencies
            token_obj = get_cryptocurrency_by_symbol_and_network(
                db=db, symbol=token.symbol, network_id=network_obj.id
            )
            if not token_obj:
                token_obj = Cryptocurrency()

            token_obj.address = token.address
            token_obj.decimals = token.decimals
            token_obj.symbol = token.symbol
            token_obj.name = token.name
            token_obj.terra_denom = token.terra_denom
            token_obj.network_id = network_obj.id
            db.add(token_obj)
            db.commit()


def init_db(db: Session):

    if settings.DEBUG:
        data_path = "data.debug.yaml"
    else:
        data_path = "data.yaml"

    with open(
        pathlib.Path(__file__).parent.parent.parent.resolve().joinpath(data_path)
    ) as f:
        data: dict = yaml.safe_load(f)
        init_data(db=db, data=data)


def create_database(db_name, user, password, host):
    # Connect to the default mssql database
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={host},{settings.MSSQL_PORT};"
        f"UID={user};"
        f"PWD={password};"
        "TrustServerCertificate=Yes"

    )
    # Connect to the MSSQL instance
    conn = pyodbc.connect(conn_str, autocommit=True)

    # Create a cursor object
    cursor = conn.cursor()

    # Create a new database using the SQL "CREATE DATABASE" statement
    cursor.execute(f"CREATE DATABASE [{db_name}]")

    # Close the cursor and connection
    cursor.close()
    conn.close()

def create_tables(db_url: str):
    engine = create_engine(db_url, connect_args={'TrustServerCertificate': 'Yes'})
    Base.metadata.create_all(engine)
