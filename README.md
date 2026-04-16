# 🎓 Skripsi Similarity Checker

Sistem berbasis AI untuk mengecek kemiripan judul skripsi menggunakan metode **Semantic Similarity (Sentence Transformers / IndoBERT)**.

---

## 🚀 Fitur Utama

- 🔍 Analisis kemiripan judul skripsi
- 📊 Menampilkan Top 5 judul paling mirip
- 📈 Menentukan jumlah judul dengan topik serupa
- 🧠 Menggunakan model NLP (Sentence Transformer)
- 📥 Download semua judul mirip dalam format CSV
- 🌐 Web interface sederhana (HTML + FastAPI)

---

## 🧠 Cara Kerja

1. Judul input diubah menjadi embedding menggunakan model:
paraphrase-multilingual-MiniLM-L12-v2
2. Dibandingkan dengan dataset menggunakan **Cosine Similarity**
3. Sistem menentukan:
- Judul mirip (≥ 0.5)
- Top hasil (≥ 0.6)
4. Output berupa:
- Persentase kemiripan
- Status kelayakan judul
- Rekomendasi

---

## 📁 Struktur Project
skripsi-similarity/
│
├── main.py
├── index.html
├── model_semantic.pkl
├── requirements.txt
├── README.md
└── venv/ (tidak diupload)

---

## ⚙️ Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/USERNAME/skripsi-similarity.git
cd skripsi-similarity

### 2. Buat Virtual Environment
python -m venv venv
Aktifkan:
Windows:
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt


▶️ Menjalankan Backend
python -m uvicorn main:app --reload
Akses API:
http://127.0.0.1:8000/docs

🌐 Menjalankan Frontend

Buka file:
index.html
di browser (double click atau Open with Browser)

📥 Download Hasil

Klik tombol:
Download Judul Mirip
File CSV akan otomatis terdownload.

📊 Output Sistem

Contoh hasil:
Jumlah judul mirip
Persentase kemiripan
Status:
❌ Terlalu umum
✅ Masih bisa dikembangkan
Top 5 judul paling mirip

⚠️ Catatan
Model pertama kali dijalankan akan mendownload ±500MB
Pastikan koneksi internet stabil
File .pkl sebaiknya tidak diupload ke GitHub jika besar

🧑‍💻 Teknologi
Python
FastAPI
Sentence Transformers
Scikit-learn
HTML + JavaScript

🎯 Penggunaan

Sistem ini digunakan untuk:
Validasi judul skripsi
Menghindari duplikasi topik
Membantu dosen / akademik

📌 Author

Dzaky Muhammad Zidane
Informatika - Universitas Sebelas Maret
