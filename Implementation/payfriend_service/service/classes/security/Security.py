import hashlib
from models import Card

class Security:
    """
    Class which provides security util methods
    Useful for: encrypting card details
    """

    @staticmethod
    def get_salted_and_hashed_plaintext(plaintext, salt):
        """
        Card details will be hashed using SHA256
        Note: This method MUTATES the passed in object
        """
        pass
        
