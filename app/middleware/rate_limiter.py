import time
from typing import Dict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 5, period: int = 60):
        super().__init__(app)
        self.calls = calls  # Number of allowed calls
        self.period = period  # Time period in seconds
        self.clients: Dict[str, list] = {}  # Store client request timestamps

    async def dispatch(self, request: Request, call_next):
        # Only apply rate limiting to POST /api/v1/short_url endpoint
        if request.method == "POST" and request.url.path == "/api/v1/short_url":
            client_ip = self._get_client_ip(request)
            current_time = time.time()
            
            # Clean old requests from the client's history
            if client_ip in self.clients:
                self.clients[client_ip] = [
                    req_time for req_time in self.clients[client_ip]
                    if current_time - req_time < self.period
                ]
            else:
                self.clients[client_ip] = []
            
            # Check if client has exceeded the rate limit
            if len(self.clients[client_ip]) >= self.calls:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Maximum {self.calls} requests per {self.period} seconds."
                )
            
            # Add current request timestamp
            self.clients[client_ip].append(current_time)
        
        response = await call_next(request)
        return response

    def _get_client_ip(self, request: Request) -> str:
        # Try to get real IP from headers first, then fallback to client host
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
