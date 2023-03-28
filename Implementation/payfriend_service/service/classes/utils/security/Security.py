import hashlib
import os
import secrets

class Security:
    """
    Class which provides security util methods
    Useful for: encrypting card details
    """

    @staticmethod
    def get_salted_and_hashed_plaintext(plaintext: str):
        """
        Hashed using SHA256 and a generated salt.
        Returns the hash and the salt which was generated for the hashing.
        """
        salt = secrets.token_hex(8)
        encodedPlainText = plaintext.encode()
        digest = hashlib.pbkdf2_hmac('sha256', encodedPlainText, salt.encode('utf-8'), 10000)
        hex_hash = digest.hex()

        return (hex_hash, salt)

    @staticmethod
    def get_hashed_with_salt(salt: bytes, plaintext: str):
        """
        Hashed using SHA256 and a given salt.
        Returns the hash.
        """
        encodedPlainText = plaintext.encode()
        digest = hashlib.pbkdf2_hmac('sha256', encodedPlainText, salt.encode('utf-8'), 10000)
        hex_hash = digest.hex()

        return hex_hash
        
