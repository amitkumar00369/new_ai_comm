

from bcrypt import hashpw,checkpw,gensalt
from dotenv import load_dotenv
from core.config import settings
load_dotenv()
SALT=settings.SALT

class passwordService:


    @staticmethod
    def createPassword(plainPassword: str) -> bytes:
        salt = gensalt()  # generate valid salt
        return  hashpw(plainPassword.encode('utf-8'), salt)

    @staticmethod
    def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
        return checkpw(plainPassword.encode('utf-8'), hashedPassword.encode('utf-8'))



PasswordService = passwordService()