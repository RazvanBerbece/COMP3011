from ...contexts.users.users_context import *
from ...utils.security.Security import Security

class AuthService():
    """
    Interface which provides methods for signing users up, checking account credentials on logins
    and other utils
    """

    @staticmethod
    def register_user(email: str, password: str):
        # Setup context
        users_context = UsersContext()
        # Process user input
        hash, salt = Security.get_salted_and_hashed_plaintext(password)
        # Store
        users_context.add_user_to_table(email, hash, salt)
        # Return status code / error
        return 0
    
    @staticmethod
    def authenticate_user(email: str, password: str):
        # Setup context
        users_context = UsersContext()
        # Retrieve salt for email
        salt = users_context.get_salt_for_email(email)
        # Compute salted hash
        hash = Security.get_hashed_with_salt(salt, password)
        # Query DB
        registered = users_context.user_is_registered(email, hash)
        # Return status code / error
        if registered:
            return True
        else:
            return False