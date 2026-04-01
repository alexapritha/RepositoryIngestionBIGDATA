# Repository Ingestion BIG DATA ANALITIK
Mini data pipeline untuk melakukan ingestion data dari MySQL (RDBMS) dan file CSV ke object storage MinIO. Project ini mencakup konfigurasi database, deployment MinIO menggunakan Docker, serta script Python untuk membaca dan menyimpan data ke dalam bucket dengan struktur raw/rdbms dan raw/csv.

[1] STRUKTUR FILE
------------------------------
- ingestion.py
  Script utama untuk proses ingestion data dari MySQL (RDBMS) dan CSV ke MinIO.

- compose.yaml
  File konfigurasi untuk menjalankan MinIO menggunakan Docker (port, credential, storage).

- DataHargaRumahDepok/
  Folder dataset CSV sebagai data uji coba ingestion.

- READ ME.txt
  Dokumentasi panduan penggunaan project.


[2] ALUR SISTEM
------------------------------
MySQL + CSV (source data)
        ↓
   ingestion.py (proses ingestion)
        ↓
MinIO (object storage)
        ↓
Struktur penyimpanan:
- raw/rdbms/
- raw/csv/


[3] STEP-BY-STEP MENJALANKAN
------------------------------
1. Pastikan Docker, Python, MySQL, dan library (pandas, pymysql, minio) sudah tersedia.

2. Jalankan MySQL dan pastikan database:
   "bigdata_minilab" sudah dibuat.

3. Sesuaikan konfigurasi koneksi di ingestion.py:
   DB_URL = mysql+pymysql://user:password@localhost:3306/bigdata_minilab

4. Pastikan dataset CSV sudah tersedia di folder project.

5. Jalankan MinIO:
   docker compose up -d

6. Jalankan proses ingestion:
   python ingestion.py

7. Verifikasi hasil:
   - Cek terminal output
   - Cek dashboard MinIO (localhost:9001)


[4] INDIKATOR KEBERHASILAN
------------------------------
- sukses RDBMS
- sukses CSV
- FINISH

Jika ketiga pesan muncul, maka seluruh proses ingestion berhasil.
```
