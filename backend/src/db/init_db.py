from src.db.manage import init_db
from src.db.session import SessionLocal


def init_database():
    db = SessionLocal()
    init_db(db=db)
    db.close()


# Initiates a new DB session
if __name__ == "__main__":
    db = SessionLocal()
    init_db(db=db)
    db.close()
