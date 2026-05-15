import os
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a',
    filename=r"C:\Users\user\Desktop\avito\logs\bi_schema.log"
)

def get_engine():
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url)

engine = get_engine()

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS ml_schema"))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS ml_schema.obt_avito(
            avito_id SERIAL PRIMARY KEY,
            titre VARCHAR,
            lien TEXT,
            ville VARCHAR,
            prix INT,
            surface INT,
            chambres INT,
            salle_de_bain INT,
            prix_m2 INT
        )
    """))

df = pd.read_csv(r"C:\Users\user\Desktop\avito\data\silver\cleaned.csv")

df.to_sql("obt_avito", engine, if_exists="append", schema="ml_schema", index=False)