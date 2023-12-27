import uuid

import redis


def get_redis_connection():
    return redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def generate_uuid():
    return str(uuid.uuid4())
