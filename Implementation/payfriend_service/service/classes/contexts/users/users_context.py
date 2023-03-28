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
    def email_exists(email: str):
        try:
            user = User.objects.get(Email=email)
            return True
        except:
            return False

    @staticmethod
    def get_salt_for_email(email: str) -> bytes:
        try:
            user = User.objects.get(Email=email)
            return user.Salt
        except:
            return None
    
    @staticmethod
    def user_is_registered(email: str, hash: str):
        try:
            user = User.objects.get(Email=email, Password=hash)
            return True
        except:
            return False

