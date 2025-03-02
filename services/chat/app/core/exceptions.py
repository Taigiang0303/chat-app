from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


class AppException(Exception):
    """Base exception class for application-specific exceptions"""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An unexpected error occurred"
    
    def __init__(self, detail: str = None, status_code: int = None):
        if detail:
            self.detail = detail
        if status_code:
            self.status_code = status_code


class AuthenticationError(AppException):
    """Exception raised for authentication errors"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication failed"


class AuthorizationError(AppException):
    """Exception raised for authorization errors"""
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not authorized to perform this action"


class ResourceNotFoundError(AppException):
    """Exception raised when a requested resource is not found"""
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"


class ResourceAlreadyExistsError(AppException):
    """Exception raised when attempting to create a resource that already exists"""
    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists"


class ValidationError(AppException):
    """Exception raised for validation errors"""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Validation error"


class WebSocketError(AppException):
    """Exception raised for WebSocket errors"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "WebSocket error"


def setup_exception_handlers(app: FastAPI):
    """Set up exception handlers for the application"""
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Validation error", "errors": exc.errors()},
        )
    
    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Validation error", "errors": exc.errors()},
        )
    
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # Log the exception here
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"},
        ) 