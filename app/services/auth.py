from passlib.hash import pbkdf2_sha256
from app.models.database import User, db

class AuthService:
    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_password(password, password_hash):
        return pbkdf2_sha256.verify(password, password_hash)

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and AuthService.verify_password(password, user.password_hash):
            return user
        return None
