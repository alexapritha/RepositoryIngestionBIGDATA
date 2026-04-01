import pandas as pd
from sqlalchemy import create_engine
from minio import Minio
from io import BytesIO
import os

# --- 1. KONFIGURASI KONEKSI ---
# MySQL (Instance MySQLAlexa)
DB_URL = "mysql+pymysql://root:Pritha*28@localhost:3306/bigdata_minilab"

# MinIO (Docker Container)
minio_client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password123",
    secure=False
)

# Lokasi file CSV from Kaggle (Data Harga Rumah Depok)
CSV_PATH = r"C:\Users\LENOVO\Documents\Big Data Analitik\DataHargaRumahDepok\Raw-Final-Rumah.csv"

# --- 2. FUNGSI UPLOAD KE MINIO ---
def upload_to_minio(df, folder_name, file_name):
    # Mengubah dataframe menjadi format CSV di dalam memori
    csv_buf = BytesIO()
    df.to_csv(csv_buf, index=False)
    csv_buf.seek(0)
    
    # Menentukan path di dalam bucket: raw/folder_name/file_name
    object_path = f"{folder_name}/{file_name}"
    
    minio_client.put_object(
        "raw", 
        object_path, 
        data=csv_buf, 
        length=len(csv_buf.getvalue()), 
        content_type='application/csv'
    )
    print(f"Sukses: Data tersimpan di raw/{object_path}")

# --- 3. EKSEKUSI INGESTION ---
try:
    # A. Pastikan Bucket 'raw' sudah ada
    if not minio_client.bucket_exists("raw"):
        minio_client.make_bucket("raw")
        print("Bucket 'raw' berhasil dibuat.")

    # B. PROSES RDBMS (Tabel Clients)
    print("Sedang menarik data dari MySQL (Tabel Clients)...")
    engine = create_engine(DB_URL)
    df_mysql = pd.read_sql("SELECT * FROM clients", engine)
    upload_to_minio(df_mysql, "rdbms", "clients_data.csv")

    # C. PROSES CSV (Data Harga Rumah Depok)
    print("Sedang membaca file CSV Kaggle...")
    if os.path.exists(CSV_PATH):
        df_csv = pd.read_csv(CSV_PATH)
        upload_to_minio(df_csv, "csv", "Raw-Final-Rumah.csv")
    else:
        print(f"ERROR: File tidak ditemukan di {CSV_PATH}")

    print("\n[FINISH] Seluruh data berhasil masuk ke MinIO!")

except Exception as e:
    print(f"Terjadi kesalahan teknis: {e}")