import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import get_settings

settings = get_settings()
security = HTTPBearer()


class AuthService:
    """
    Valida el JWT emitido por AUTH-SERVICE (Java).
    Este módulo NO crea usuarios, NO genera tokens.
    """

    def __init__(self):
        self.secret = settings.JWT_SECRET
        self.algorithm = settings.JWT_ALGORITHM
        self.issuer = settings.JWT_ISSUER

    def validate_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                options={"verify_aud": False},
            )
            if payload.get("iss") != self.issuer:
                raise jwt.InvalidIssuerError("Invalid issuer")
            return payload
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )


auth_service = AuthService()


def get_current_user(credentials: HTTPAuthorizationCredentials = security):
    # Modo desarrollo: permite omitir validación real
    if settings.DISABLE_AUTH:
        return {"sub": "demo@local", "roles": ["DEMO"]}
    return auth_service.validate_token(credentials.credentials)