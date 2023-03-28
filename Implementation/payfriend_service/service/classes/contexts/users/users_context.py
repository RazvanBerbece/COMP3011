from ....models import User

class UsersContext:
    """
    DB Context interface.
    Manages connecting to the sqlite3 DB and querying the Users table
    """

    @staticmethod
    def add_user_to_table(email: str, hash: str, salt: str):
        user = User(Email=email, Password=hash, Salt=salt)
        user.save()

    @staticmethod
    def get_salt_for_email(email: str):
        pass
    
    @staticmethod
    def user_is_registered(email: str, hash: str):
        pass

