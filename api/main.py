import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database import create_table, save_score, get_all_scores

app = FastAPI()
handler = app

class ScoreData(BaseModel):
    ad_soyad: str
    skor: int
    toplam: int
    tarih: str

@app.on_event("startup")
def startup():
    try:
        create_table()
    except Exception as e:
        print(f"create_table hatası: {e}")

@app.post("/skor-kaydet")
def skor_kaydet(data: ScoreData):
    save_score(data.ad_soyad, data.skor, data.toplam, data.tarih)
    return {"mesaj": "Kaydedildi"}

@app.get("/skorlar")
def skorlar():
    rows = get_all_scores()
    return [{"ad_soyad": r[0], "skor": r[1], "tarih": r[2]} for r in rows]

# Yukarıdaki route'lar tanımlandıktan SONRA mount edilmeli;
# aksi halde statik dosya servisi diğer route'ların önüne geçer.
FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")