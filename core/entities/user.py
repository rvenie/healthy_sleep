class User:
    def __init__(self, id=None, username=None, password_hash=None, email=None, credits=100):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.credits = credits