import requests
import pandas as pd
import psycopg2 # type: ignore
import os

def extract():
    url = "https://api.open-meteo.com/v1/forecast?latitude=0&longitude=110&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['hourly'])
    return df

def transform(df):
    df['time'] = pd.to_datetime(df['time'])
    df = df.rename(columns={'temperature_2m': 'temperature'})
    return df

def load(df):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS weather")
    cur.execute("CREATE TABLE weather (time TIMESTAMP, temperature FLOAT)")
    
    for _, row in df.iterrows():
        cur.execute("INSERT INTO weather VALUES (%s, %s)", (row['time'], row['temperature']))
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    df = extract()
    df = transform(df)
    load(df)
