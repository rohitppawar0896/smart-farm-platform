from app.modules.users.models import User
from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def has_password(password: str) -> str:
    sha256_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.hash(sha256_hash)


# verify_password - This method used to verify the entered password is correct or not
# For this it first coverts the passowrd int hash and match to the hash present in database.
# It returns Boolean value


def verify_password(password: str, hashed_password: str) -> bool:
    sha256_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)


def create_user(db, user_data):
    user = User(
        email=user_data.email,
        password_hash=has_password(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
