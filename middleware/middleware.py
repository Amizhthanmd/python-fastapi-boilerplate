from typing import Optional
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from jose import JWTError, jwt
from config.settings import settings

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method

        if path in ["/api/v1/auth/login", "/docs", "/openapi.json"] or method == "OPTIONS":
            return await call_next(request)

        token: Optional[str] = None
        
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[len("Bearer "):]
        else:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            request.state.user = payload
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        response: Response = await call_next(request)
        return response
