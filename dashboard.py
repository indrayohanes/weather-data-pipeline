import streamlit as st
import pandas as pd
import psycopg2
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi koneksi
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "weatherdb"),
    "user": os.getenv("DB_USER", "weatheruser"),
    "password": os.getenv("DB_PASS", "weatherpass"),
    "port": 5432
}

# Load data dari PostgreSQL
@st.cache_data
def load_data():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM weather", conn)
    conn.close()
    df['time'] = pd.to_datetime(df['time'])
    return df

# Mulai tampilan dashboard
st.title("🌤️ Weather Dashboard")
df = load_data()
st.write("Jumlah data:", len(df))
st.write(df.head())

# Tampilkan data mentah
if st.checkbox("Tampilkan data mentah"):
    st.dataframe(df)

# Line Chart
st.subheader("Tren Suhu Seiring Waktu")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=df, x="time", y="temperature", ax=ax)
ax.set_xlabel("Waktu")
ax.set_ylabel("Suhu (°C)")
st.pyplot(fig)

# Rata-rata suhu per jam
st.subheader("📊 Rata-Rata Suhu per Jam")
df['hour'] = df['time'].dt.hour
hourly_avg = df.groupby('hour')['temperature'].mean().reset_index()

st.bar_chart(hourly_avg.set_index('hour'))

# Filter suhu minimum
min_temp = st.slider("Tampilkan data suhu di atas:", min_value=float(df['temperature'].min()), max_value=float(df['temperature'].max()), value=10.0)
filtered_df = df[df['temperature'] > min_temp]

st.subheader(f"Data dengan suhu di atas {min_temp}°C")
st.dataframe(filtered_df)

try:
    st.subheader("Tren Suhu Seiring Waktu")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df, x="time", y="temperature", ax=ax)
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Suhu (°C)")
    st.pyplot(fig)
except Exception as e:
    st.error(f"Gagal memuat grafik suhu: {e}")
