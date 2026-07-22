from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging

logger = logging.getLogger(__name__)

# Rate limiter using client IP
# For a load-balanced production environment, you might use X-Forwarded-For headers
limiter = Limiter(key_func=get_remote_address, default_limits=["1000/minute"])

def add_rate_limiter(app: FastAPI):
    """
    Attach SlowAPI rate limiter to the FastAPI application to defend against massive spikes.
    If requests exceed 1000 per minute per IP, it throws a 429 Too Many Requests,
    protecting the underlying DB connection pool from exhaustion.
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info("Rate limiter (SlowAPI) initialized and attached to FastAPI app.")
