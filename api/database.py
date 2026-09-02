import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL ortam değişkeni bulunamadı. Vercel > Settings > Environment Variables kısmını kontrol et.")
    if "sslmode" not in dsn:
        dsn += "?sslmode=require" if "?" not in dsn else "&sslmode=require"
    return psycopg2.connect(dsn)

def create_table():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS katilimcilar (
                id SERIAL PRIMARY KEY,
                ad_soyad TEXT,
                tarih TEXT
            )
        """)
        conn.commit()
    finally:
        cur.close()
        conn.close()

def save_katilimci(ad_soyad, tarih):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO katilimcilar (ad_soyad, tarih) VALUES (%s, %s)",
            (ad_soyad, tarih)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_all_katilimcilar():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT ad_soyad, tarih FROM katilimcilar")
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()