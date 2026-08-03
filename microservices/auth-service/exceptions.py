from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

class UserExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class UserNotVerifiedError(Exception):
    pass

class VerificationCodeInvalidError(Exception):
    pass

def register_handlers(app: FastAPI):
    @app.exception_handler(UserExistsError)
    def user_exists_handler(request: Request, exc: UserExistsError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "User with this email already exists"},
        )

    @app.exception_handler(InvalidCredentialsError)
    def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid email or password"},
        )

    @app.exception_handler(UserNotVerifiedError)
    def user_not_verified_handler(request: Request, exc: UserNotVerifiedError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "User account is not verified yet. Please verify using code."},
        )

    @app.exception_handler(VerificationCodeInvalidError)
    def verification_code_invalid_handler(request: Request, exc: VerificationCodeInvalidError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid or expired verification code"},
        )
