import pandas as pd
import psycopg2
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi koneksi PostgreSQL dari .env atau default
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "weatherdb"),
    "user": os.getenv("DB_USER", "weatheruser"),
    "password": os.getenv("DB_PASS", "weatherpass"),
    "port": 5432
}

# Koneksi ke database
conn = psycopg2.connect(**DB_CONFIG)

# Ambil data cuaca
df = pd.read_sql("SELECT * FROM weather", conn)
conn.close()

# Proses data
df['time'] = pd.to_datetime(df['time'])
df = df.set_index('time')

# --- VISUALISASI ---

# 1. Grafik suhu dari waktu ke waktu
plt.figure(figsize=(12, 5))
sns.lineplot(data=df, x=df.index, y='temperature')
plt.title("Tren Suhu dari Waktu ke Waktu")
plt.xlabel("Waktu")
plt.ylabel("Suhu (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Rata-rata suhu per jam
df['hour'] = df.index.hour
hourly_avg = df.groupby('hour')['temperature'].mean()

plt.figure(figsize=(10, 5))
sns.barplot(x=hourly_avg.index, y=hourly_avg.values, palette="coolwarm")
plt.title("Rata-Rata Suhu per Jam")
plt.xlabel("Jam")
plt.ylabel("Suhu (°C)")
plt.tight_layout()
plt.show()
