// Import modul Express untuk membuat server HTTP
const express = require('express');
// Import modul mysql untuk koneksi ke database MySQL
const mysql = require('mysql');
// Inisialisasi Express app
const app = express();
// Port yang digunakan oleh server
const port = 3000;

// Konfigurasi koneksi ke database MySQL
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'app_provis'
});

// Membuat koneksi ke database
db.connect((err) => {
  if (err) throw err;
  console.log('Database connected');
});

// Endpoint untuk mendaftar (signup)
app.post('/signup', (req, res) => {
  // Mendapatkan data dari body permintaan
  const { username, password } = req.body;
  // Lakukan operasi untuk menyimpan data pengguna ke database
  db.query('INSERT INTO users (username, password) VALUES (?, ?)', [username, password], (err, result) => {
    if (err) {
      res.status(500).json({ message: 'Failed to signup' });
    } else {
      res.status(200).json({ message: 'User signed up successfully' });
    }
  });
});

// Endpoint untuk login
app.post('/login', (req, res) => {
    // Mendapatkan data dari body permintaan
    const { username, password } = req.body;
    // Lakukan operasi untuk memeriksa kredensial pengguna dari database
    db.query('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], (err, result) => {
      if (err) {
        res.status(500).json({ message: 'Internal server error' });
      } else {
        // Jika data pengguna ditemukan, kirim respons berhasil
        if (result.length > 0) {
          res.status(200).json({ message: 'User logged in successfully' });
        } else {
          // Jika tidak ditemukan, kirim respons gagal
          res.status(401).json({ message: 'Invalid credentials' });
        }
      }
    });
  });

// Membuat endpoint API untuk mendapatkan daftar dokter
app.get('/doctor', (req, res) => {
  // Menjalankan query untuk mengambil data dokter dari database
  db.query('SELECT * FROM doctor', (err, result) => {
    if (err) throw err;
    // Mengirim data dokter sebagai respons JSON
    res.json(result);
  });
});

// Mendengarkan permintaan di port tertentu
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});