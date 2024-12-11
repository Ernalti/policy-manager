from .. import db, flask_bcrypt

class User(db.Model):
    """User model for storing user-related details."""
    __tablename__ = 'users'

    # Unique identifier for each user
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Username must be unique and not null
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Email for the user, also unique and not null
    email = db.Column(db.String(255), unique=True, nullable=True)
    # Hashed password stored securely
    password_hash = db.Column(db.String(128), nullable=False)
    # Date and time when the user registered

    @property
    def password(self):
        """Password is a write-only field."""
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        """Hashes the password and stores it securely."""
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Compares the provided password with the stored hash."""
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """String representation of the user object."""
        return f"<User '{self.username}'>"

    def to_dict(self):
        """Метод для конвертации модели в словарь."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
