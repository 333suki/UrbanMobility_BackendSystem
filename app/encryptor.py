import os
from cryptography.fernet import Fernet
import dotenv
import hashlib

dotenv.load_dotenv()

class Encryptor:
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("Encryption key is missing from environment variables.")
    fernet = Fernet(key.encode())

    @staticmethod
    def encrypt(data: str) -> str | None:
        if not data:
            return None
        return Encryptor.fernet.encrypt(data.encode()).decode()

    @staticmethod
    def decrypt(token: str) -> str | None:
        if not token:
            return None
        return Encryptor.fernet.decrypt(token.encode()).decode()

    @staticmethod
    def get_hash(data: str):
        return hashlib.sha256(data.encode()).hexdigest()
