from datetime import datetime


def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()
