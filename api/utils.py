import jwt
import datetime
from configs.config import settings


def generate_access_token(id):
    expired = settings.jwt_access_expire_time
    if not expired:
        expired = 5
    access_token_payload = {
        "user_id": id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=expired),
        "iat": datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return access_token


def generate_refresh_token(id):
    expired = settings.jwt_refresh_expire_time
    if not expired:
        expired = 30
    refresh_token_payload = {
        "user_id": id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=expired),
        "iat": datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )

    return refresh_token


def jwt_decode(token, verify=True):
    decoded = jwt.decode(
        token,
        key=settings.SECRET_KEY,
        algorithms="HS256",
        options={"verify_signature": verify},
    )
    return decoded
