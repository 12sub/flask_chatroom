from werkzeug.security import check_password_hash

class User:
    def __init__(self, username, email, password) -> None:
        self.username = username
        self.email = email
        self.password = password
    
    @staticmethod    
    def is_authenticated(self):
        return True
    
    @staticmethod 
    def is_active(self):
        return True
    
    @staticmethod 
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.username
    
    def check_pass(self, password_input):
        return check_password_hash(self.password, password_input)