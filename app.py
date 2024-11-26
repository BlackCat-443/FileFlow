import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from models import db, User
import mimetypes
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load .env file
load_dotenv()

app = Flask(__name__)

# Konfigurasi aplikasi
app.secret_key = os.getenv('app.secret_key', 'default_secret_key')  # Tambahkan default untuk fallback
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/user'  # Sesuaikan dengan xampp
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'backups'

# Inisialisasi database
db.init_app(app)

# Buat tabel jika belum ada
with app.app_context():
    db.create_all()

# Inisialisasi folder backup utama
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CATEGORIES = {
    'photos': ['image/jpeg', 'image/png', 'image/gif'],
    'documents': ['application/pdf', 'application/msword', 'text/plain'],
    'videos': ['video/mp4', 'video/x-matroska'],
    'others': []
}

# Membuat subfolder untuk setiap kategori file
for category in CATEGORIES.keys():
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], category), exist_ok=True)

def get_user_upload_folder():
    """Mengambil folder upload untuk pengguna yang login berdasarkan email dan ID pengguna."""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        
        # Mengamankan email agar bisa digunakan dalam nama folder
        email_safe = secure_filename(user.email)  # Amankan email agar tidak ada karakter ilegal
        
        # Membuat nama folder berdasarkan ID dan email pengguna
        user_folder_name = f"{user.id}_{email_safe}"
        
        # Membuat folder untuk pengguna
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_folder_name)
        os.makedirs(user_folder, exist_ok=True)  # Buat folder pengguna jika belum ada

        # Buat folder kategori untuk pengguna ini jika belum ada
        for category in CATEGORIES.keys():
            os.makedirs(os.path.join(user_folder, category), exist_ok=True)

        return user_folder
    return None

def get_file_category(file_path):
    """Menentukan kategori file berdasarkan MIME type."""
    mime_type, _ = mimetypes.guess_type(file_path)
    for category, mime_types in CATEGORIES.items():
        if mime_type in mime_types:
            return category
    return 'others'

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_folder = get_user_upload_folder()
    if user_folder:
        files = {
            category: os.listdir(os.path.join(user_folder, category))
            for category in CATEGORIES.keys()
        }
        return render_template('index.html', files=files)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.check_password(password):
                session['user_id'] = user.id
                session['user_email'] = user.email  # Menyimpan email ke session
                flash('You have successfully logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid password. Please try again.', 'error')
        else:
            flash('User not found. Please check your email.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password == confirm_password:
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'error')
                return redirect(url_for('register'))
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if 'files[]' not in request.files:
        flash('No files selected.', 'error')
        return redirect(url_for('home'))
    files = request.files.getlist('files[]')
    user_folder = get_user_upload_folder()
    for file in files:
        if file.filename:
            category = get_file_category(file.filename)
            category_folder = os.path.join(user_folder, category)
            os.makedirs(category_folder, exist_ok=True)  # Pastikan folder kategori ada
            save_path = os.path.join(category_folder, file.filename)
            file.save(save_path)
    flash('Files uploaded successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/delete/<category>/<filename>', methods=['POST'])
def delete_file(category, filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_folder = get_user_upload_folder()
    if user_folder:
        file_path = os.path.join(user_folder, category, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash('File deleted successfully.', 'success')
        else:
            flash('File not found.', 'error')
    return redirect(url_for('home'))

@app.route('/download/<category>/<filename>', methods=['GET'])
def download_file(category, filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_folder = get_user_upload_folder()
    if user_folder:
        return send_from_directory(
            os.path.join(user_folder, category),
            filename,
            as_attachment=True
        )

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050)
