

from bcrypt import hashpw,checkpw,gensalt
from dotenv import load_dotenv
from core.config import settings
load_dotenv()
SALT=settings.SALT
print(SALT)

class passwordService:


    @staticmethod
    def createPassword(plainPassword: str) -> str:
        salt = gensalt()
        hashed = hashpw(plainPassword.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
        return checkpw(
            plainPassword.encode('utf-8'),
            hashedPassword.encode('utf-8'))



PasswordService = passwordService()