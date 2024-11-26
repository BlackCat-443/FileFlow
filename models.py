from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # Nama tabel di database
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        """Hash dan simpan password pengguna menggunakan pbkdf2:sha256."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Periksa apakah password yang dimasukkan cocok dengan hash yang ada di database."""
        return check_password_hash(self.password_hash, password)

def init_db():
    """Hanya untuk membuat tabel, tanpa inisialisasi ulang db."""
    with db.engine.connect() as connection:
        connection.execute("SELECT 1")  # Tes koneksi ke database
