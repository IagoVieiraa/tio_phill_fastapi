from ..utils.hash_password import hash_password
from ..models.user_model import User
from ..repositories import user_repository

def service_create_user(**user_credentials):
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

        if email is None or not isinstance(email, str):
            return {"success": False, "body": "Email format is invalid.", "status_code": 401}
        if pw is None or not isinstance(pw, str):
            return {"success": False, "body": "Password format is invalid", "status_code": 402}
        
        hashed_pw = hash_password(pw)
        new_user = User(email=user_credentials.get("email"), hashed_password=hashed_pw)

        created_user = user_repository.create_user(new_user)

        return {"success": True, "body": f"User {created_user.email}  created successfuly", "status_code": 201, "id": str(created_user.id)}
    except Exception as ex:
        print(ex)
        return {"success": False, "body": "Error occurred in create_user","status_code": 500}