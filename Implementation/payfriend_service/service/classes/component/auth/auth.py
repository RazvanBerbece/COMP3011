from ...contexts.users.users_context import *

from ...utils.security.Security import Security
from ...utils.validation.validation import Validation

class AuthComponent():
    """
    Interface which provides methods for signing users up, checking account credentials on logins
    and other utils
    """

    def __init__(self):
        self.users_context = UsersContext()

    def register_user(self, email: str, password: str):
        """
        Registers a user on the service by storing account details. Performs validation of input data, mainly that the
        email is a valid email address and that the password is somewhat secure.
        Returns:
        - `-3` if provided password doesn't match service standards
        - `-2` if provided email address is invalid
        - `-1` if account with given email already exists
        - `0` if credentials are valid and the user can register
        """
        # Validate user input
        if Validation.is_valid_email_address(email) == False:
            return -2
        if Validation.is_valid_password(password) == False:
            return -3
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
        """
        Authenticates a pair of account credentials on the service. Performs validation of input data, mainly that the
        email is a valid email address and that the password matches the standards.
        Returns:
        - `-3` if provided email address is invalid
        - `-2` if provided password doesn't match service standards
        - `-1` if account does not exist
        - `0` if credentials match and the user can log in
        """
        # Validate user input
        if Validation.is_valid_email_address(email) == False:
            return -2
        if Validation.is_valid_password(password) == False:
            return -3
        # Retrieve salt for email
        salt = self.users_context.get_salt_for_email(email)
        if salt == None:
            return -1
        # Compute salted hash
        hash = Security.get_hashed_with_salt(salt, password)
        # Query DB
        registered = self.users_context.user_is_registered(email, hash)
        # Return status code / error
        if registered:
            return 0
        else:
            return -1