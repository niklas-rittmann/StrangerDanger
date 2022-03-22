from datetime import datetime, timedelta
from typing import NewType

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from stranger_danger.constants.settings import AuthSettings

Token = NewType("Token", str)


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = AuthSettings().SECRET

    def get_password_hash(self, password: str) -> str:
        """Return hashed password"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        """Check if passwords are equal"""
        return self.pwd_context.verify(plain, hashed)

    def encode_token(self, user_id: int) -> Token:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token: Token) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(Token(auth.credentials))


auth_handler = AuthHandler()
