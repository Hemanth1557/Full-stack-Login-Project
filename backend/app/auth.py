from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed):
    return pwd_context.verify(plain_password, hashed)

def hash_password(password):
    return pwd_context.hash(password)
