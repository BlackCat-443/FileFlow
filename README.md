
# Aplikasi FileFlow 

FileFlow adalah aplikasi untuk mengelola unggahan file secara efisien dengan fitur cloud storage. Aplikasi ini memungkinkan pengguna untuk mengunggah file, memantau progres unggahan, serta mengelola akun pengguna untuk login dan registrasi. FileFlow menggunakan teknologi modern untuk pengalaman yang responsif dan interaktif.


## 🔧 Konfigurasi dan Pengaturan

### 1. **Instalasi Dependencies**
Pastikan Anda telah menginstal semua dependensi yang dibutuhkan menggunakan `pip`. Jalankan perintah berikut untuk menginstalnya:

```bash
pip install -r requirements.txt
```

### 2. **Pengaturan Secret Key**
Aplikasi ini membutuhkan **SECRET_KEY** untuk keperluan session pada Flask. Jika Anda ingin menggunakan `SECRET_KEY` yang berbeda, Anda bisa membuatnya secara manual menggunakan Python:

```python
import os
print(os.urandom(24))
```

Salin hasil output dan tambahkan ke dalam file konfigurasi Flask Anda (misalnya `.env` atau langsung di `app.py`):

```python
app.config['SECRET_KEY'] = 'hasil_output_tadi'
```

### 3. **Mengatur Database di Laragon**
Aplikasi ini menggunakan database MySQL yang dapat Anda atur dengan mudah di Laragon. Berikut adalah langkah-langkahnya:

1. **Buka Laragon** dan pastikan MySQL sedang berjalan.
2. Klik pada tombol **Database** di Laragon dan pilih **phpMyAdmin**.
3. Buat database baru dengan nama yang Anda inginkan (misalnya `login_db`).
4. Sesuaikan konfigurasi database di aplikasi Anda. Pada file `app.py` atau di tempat konfigurasi database, masukkan pengaturan berikut:

```python
SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/login_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Pastikan Anda mengganti `password` dengan password MySQL yang sesuai.

### 4. **Menjalankan Aplikasi**
Setelah semua konfigurasi selesai, Anda bisa menjalankan aplikasi dengan perintah berikut:

```bash
flask run
```

Aplikasi akan berjalan di `http://127.0.0.1:5050`.

## 📁 Struktur Folder
- **app.py**: File utama aplikasi Flask.
- **templates/**: Folder untuk template HTML (Login, Register, dll).
- **static/**: Folder untuk file statis (CSS, JS, dll).
- **requirements.txt**: Daftar dependensi yang dibutuhkan aplikasi.

project-folder/
│
├── __pycache__/
│   └── models.cpython-313.pyc
│
├── backups/
│
├── instance/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── login.html
│   └── register.html
│
├── .env
├── app.py
├── models.py
├── requirements.txt
└── users.db


## 📢 Catatan
- Pastikan Laragon sudah berjalan dengan benar dan database telah dikonfigurasi dengan tepat.
- Jangan lupa untuk membuat `SECRET_KEY` yang aman untuk melindungi session aplikasi Anda.
- sweetalert nya masih bug dan jika bisa di benerin akan segera di benerin

Terima kasih telah menggunakan aplikasi ini! 😃
