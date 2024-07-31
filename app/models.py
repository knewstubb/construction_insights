from app import db
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    highlights = db.Column(db.Text, nullable=False)
    lowlights = db.Column(db.Text, nullable=False)
    emerging_issues = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(19), nullable=False)  # '2024-07-30 15:26:39'
    weather = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Feedback('{self.timestamp}', '{self.weather}')"
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
# Comments:
# 1. We import UserMixin from flask_login for handling user authentication.
# 2. We import password hashing functions from werkzeug.security.
# 3. The User model includes fields for id, username, email, password_hash, and role.
# 4. set_password method hashes the password before storing it.
# 5. check_password method verifies a given password against the stored hash.