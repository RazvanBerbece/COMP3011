from ...contexts.users.users_context import *
from ...utils.security.Security import Security

class AuthComponent():
    """
    Interface which provides methods for signing users up, checking account credentials on logins
    and other utils
    """

    def __init__(self):
        self.users_context = UsersContext()

    def register_user(self, email: str, password: str):
        # Process user input
        hash, salt = Security.get_salted_and_hashed_plaintext(password)
        # Check whether user already exists
        exists = self.users_context.email_exists(email)
        # Store
        if (exists == False):
            self.users_context.add_user_to_table(email=email, hash=hash, salt=salt)
            return 0
        # Return status code / error
        return -1
    
    def authenticate_user(self, email: str, password: str):
        # Retrieve salt for email
        salt = self.users_context.get_salt_for_email(email)
        if salt == None:
            return False
        # Compute salted hash
        hash = Security.get_hashed_with_salt(salt, password)
        # Query DB
        registered = self.users_context.user_is_registered(email, hash)
        # Return status code / error
        if registered:
            return True
        else:
            return False