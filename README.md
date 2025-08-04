
====================================================
README - FB Brute Force (Versi Uji Coba)
====================================================

📌 DESKRIPSI:
Script ini merupakan versi uji coba sederhana dari tool brute force login akun Facebook berbasis UID.
Script ini menggunakan Selenium WebDriver dengan Chrome untuk mencoba berbagai kombinasi password dari nama profil target.

🚨 CATATAN:
Script ini hanya untuk tujuan edukasi dan pengujian pribadi. Penyalahgunaan untuk hal ilegal sangat dilarang!
Script *tidak memiliki deteksi CAPTCHA penuh*, sehingga jika login sukses namun muncul error atau gagal login — kemungkinan besar halaman login menampilkan CAPTCHA.

⚙️ FITUR UTAMA:
- 🔍 Ambil nama lengkap dari link profil Facebook target.
- 🔐 Buat kombinasi password berdasarkan nama depan, belakang, dan daftar keyword.
- 🧠 Gunakan daftar password umum seperti "bismillah", "iloveyou123", dll.
- 🧪 Coba semua password yang dihasilkan satu per satu.
- ✅ Simpan akun yang berhasil login ke file `akun_berhasil.txt`.
- 🧹 Otomatis hapus profil Chrome sementara setelah tiap target.
- 🎭 Gunakan user-agent acak untuk tiap percobaan.

📁 STRUKTUR FILE YANG DIBUTUHKAN:
- `targets.txt` : berisi daftar target dengan format: LINK_PROFIL|UID
Contoh:
https://web.facebook.com/abc.defg.123|abc.defg.123

- `akun_berhasil.txt` : hasil UID dan password akun yang berhasil login akan disimpan di sini.

🛠️ DEPENDENSI YANG HARUS DIINSTALL:

```bash
pip install selenium webdriver-manager colorama pyfiglet
```

✅ DIREKOMENDASI:
- Python 3.9+
- Google Chrome versi terbaru

🚫 CATATAN PENTING:
- Script tidak mendeteksi semua jenis verifikasi seperti CAPTCHA atau checkpoint secara detail.
- Jika terjadi error saat proses, itu bisa jadi karena CAPTCHA.
- Disarankan untuk menambahkan delay lebih panjang jika digunakan pada banyak target.
- akun berhasil bisa juga di sebabkan captcha yang tidak terdeteksi jadi harap cek manual akun yang berhasil

🧪 MODE PENGUJIAN:
Script ini masih dalam versi awal/uji coba:
- Belum mendukung login multi-akun secara paralel.
- Masih menggunakan metode deteksi nama sederhana.

💡 PENGGUNAAN:
Cukup jalankan script dengan:

```bash
python namascript.py
```

📌 KREDIT:
Uji coba

====================================================
