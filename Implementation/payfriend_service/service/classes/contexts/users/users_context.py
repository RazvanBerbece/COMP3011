class UsersContext:
    """
    DB Context interface.
    Manages connecting to the sqlite3 DB and querying the Users table
    """

    def __init__(self):
        pass

    def add_user_to_table(email: str, hash: str, salt: str):
        pass

    def get_salt_for_email(email: str):
        pass

    def user_is_registered(email: str, hash: str):
        pass

