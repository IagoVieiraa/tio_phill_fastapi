from ..utils.hash_password import hash_password
from ..models.user_model import User
from ..repositories import user_repository
from datetime import timedelta, timezone
from passlib.context import CryptContext
from ..utils.handle_jwt import create_access_token
from jose import jwt, JWTError
from fastapi import HTTPException, status
from datetime import datetime
from ..core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(**user_credentials):
    try:
        """
            Creates a User object. Validates the data received from the route and calls the Repository class to create the obj in the DB

            Params:
                - user_credentials: dict["email": str, "password": str]
            
            Returns:
                - dict["success": bool, "body": str, "status_code" Integer]

        """
        email = user_credentials.get("email")
        pw = user_credentials.get("password")

        if user_repository.get_user_by_email(email):
            return {"success": False, "body": "Email already exists. Please, log-in with your email", "status_code": 400}

        if email is None or not isinstance(email, str):
            return {"success": False, "body": "Email format is invalid.", "status_code": 400}
        if pw is None or not isinstance(pw, str):
            return {"success": False, "body": "Password format is invalid", "status_code": 400}
        
        hashed_pw = hash_password(pw)
        new_user = User(email=user_credentials.get("email"), hashed_password=hashed_pw)

        created_user = user_repository.create_user(new_user)

        return {"success": True, "body": f"User {created_user.email}  created successfuly", "status_code": 201, "id": str(created_user.id)}
    except Exception as ex:
        print(ex)
        return {"success": False, "body": "Error occurred in create_user","status_code": 500}
    
def login(**user_credentials):
    user = authenticate_user(user_credentials)
    if not user:
        return None
    token_expires = timedelta(minutes=30)
    token = create_access_token({"sub": user.email}, token_expires)
    return token

def authenticate_user(user_credentials: dict):
    user = user_repository.get_user_by_email(user_credentials["email"])
    if user and verify_password(user_credentials["password"], user.hashed_password):
        return user
    else:
        return None

def verify_password(received_password, hashed_password):
    return pwd_context.verify(received_password, hashed_password)

def check_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Checa expiração
        exp = payload.get("exp")
        if exp:
            exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
            if datetime.now(timezone.utc) > exp_datetime:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expirado"
                )

        user = user_repository.get_user_by_email(payload.get("sub"))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        return {"success": True, "body": {"user_id": user.id, "user_email": user.email}, "status_code": 200}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )