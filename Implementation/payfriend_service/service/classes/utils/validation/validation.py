import re

class Validation:
    """
    Class which provides user input validation util methods.
    """

    @staticmethod
    def is_valid_email_address(email: str):
        email_address_regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
        if re.fullmatch(email_address_regex, email):
            return True
        else:
            return False
        
    @staticmethod
    def is_valid_password(password: str):
        if (len(password) < 8):
            return False
        return True
    
    @staticmethod
    def is_valid_transaction(transaction: object):
        if (transaction["city"] == "" or transaction["postcode"] == "" or transaction["country"] == "" or transaction["currency"] == ""):
            return False
        return True