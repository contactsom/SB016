class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    def update_email(self, new_email):
        if '@' in new_email and '.' in new_email:
            self.email = new_email
            return True
        return False

    def update_password(self, new_password):
        if len(new_password) >= 8:
            self.password = new_password
            return True
        return False

    def validate_credentials(self, email, password):
        return self.email == email and self.password == password

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Email: {self.email}"
