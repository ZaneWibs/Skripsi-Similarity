from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# tambahan untuk download
from fastapi.responses import StreamingResponse
import io
import pandas as pd

# =========================
# INIT APP
# =========================
app = FastAPI()

# =========================
# CORS
# =========================
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LOAD MODEL
# =========================
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

with open("model_semantic.pkl", "rb") as f:
    embeddings, df = pickle.load(f)

# =========================
# REQUEST BODY
# =========================
class RequestData(BaseModel):
    nama: str
    nim: str
    judul: str

# =========================
# LABEL
# =========================
def label_similarity(score):
    if score >= 0.8:
        return "Sangat Mirip"
    elif score >= 0.6:
        return "Mirip"
    elif score >= 0.4:
        return "Kurang Relevan"
    else:
        return "Tidak Relevan"

# =========================
# ANALISIS
# =========================
@app.post("/analisis")
def analisis(req: RequestData):

    input_embedding = model.encode([req.judul])
    similarity = cosine_similarity(input_embedding, embeddings).flatten()

    # 🔥 FIX numpy → float
    similarity = similarity.astype(float)

    max_score = float(max(similarity))

    # OUT OF DOMAIN
    if max_score < 0.5:
        return {
            "nama": req.nama,
            "nim": req.nim,
            "judul": req.judul,
            "narasi": "Judul Anda berada di luar domain dataset yang tersedia.",
            "status": "⚠️ Tidak ada pembanding relevan",
            "top": [],
            "jumlah": 0
        }

    # ======================
    # TOP RESULT
    # ======================
    top_indices = similarity.argsort()[-10:][::-1]

    top_results = []
    for idx in top_indices:
        score = float(similarity[idx])

        if score >= 0.6:
            top_results.append({
                "judul": df.iloc[idx]["judul"],
                "score": float(round(score * 100, 2)),
                "label": label_similarity(score)
            })

    # ======================
    # SEMUA MIRIP
    # ======================
    matched_indices = np.where(similarity >= 0.5)[0]

    jumlah = int(len(matched_indices))
    total = int(len(df))
    persen = float(round((jumlah / total) * 100, 2))

    # STATUS
    if jumlah >= 40:
        status = "❌ Judul terlalu umum"
    else:
        status = "✅ Judul masih bisa dikembangkan"

    narasi = f"Ditemukan {jumlah} judul dengan topik serupa ({persen}% dari dataset)."

    return {
        "nama": req.nama,
        "nim": req.nim,
        "judul": req.judul,
        "narasi": narasi,
        "status": status,
        "top": top_results,
        "jumlah": jumlah
    }

# =========================
# DOWNLOAD CSV
# =========================
@app.post("/download")
def download(req: RequestData):

    input_embedding = model.encode([req.judul])
    similarity = cosine_similarity(input_embedding, embeddings).flatten()
    similarity = similarity.astype(float)

    matched_indices = np.where(similarity >= 0.5)[0]

    hasil = df.iloc[matched_indices][["judul"]].copy()
    hasil["similarity"] = [
        float(round(similarity[i] * 100, 2)) for i in matched_indices
    ]

    # optional ranking
    hasil["ranking"] = range(1, len(hasil) + 1)

    # buat CSV di memory
    stream = io.StringIO()
    hasil.to_csv(stream, index=False)

    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv"
    )

    response.headers["Content-Disposition"] = "attachment; filename=judul_mirip.csv"

    return response