import hashlib
from models import Card

# Class which provides security util methods
# Useful for: encrypting card details
class Security:

    @staticmethod
    def encrypt_card_details(card: Card):
        # Card details will be hashed using SHA256
        # Note: This method MUTATES the passed in object
        card.card_number = hashlib.sha256(card.card_number).hexdigest()
        card.expiration_date = hashlib.sha256(card.expiration_date.strftime("%m/%d/%Y, %H:%M:%S")).hexdigest()
        card.name = hashlib.sha256(card.name).hexdigest()
        
