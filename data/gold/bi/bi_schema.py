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
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS bi_schema"))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS bi_schema.infos (
            titre_id SERIAL PRIMARY KEY,
            titre VARCHAR,
            lien TEXT
        )
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS bi_schema.regions (
            ville_id SERIAL PRIMARY KEY,
            ville VARCHAR
        )
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS bi_schema.fact_avito (
            avito_id SERIAL PRIMARY KEY,
            titre_id INT,
            ville_id INT,
            prix INT,
            surface INT,
            chambres INT,
            salle_de_bain INT,
            prix_m2 INT,
            FOREIGN KEY (titre_id) REFERENCES bi_schema.infos(titre_id),
            FOREIGN KEY (ville_id) REFERENCES bi_schema.regions(ville_id)
        )
    """))

df = pd.read_csv(r"C:\Users\user\Desktop\avito\data\silver\cleaned.csv")

df_infos = df[["titre", "lien"]].drop_duplicates()
df_regions = df[["ville"]].drop_duplicates()

df_infos.to_sql("infos", engine, if_exists="append", schema="bi_schema", index=False)
df_regions.to_sql("regions", engine, if_exists="append", schema="bi_schema", index=False)

df_infos = pd.read_sql("SELECT * FROM bi_schema.infos", engine)
df_regions = pd.read_sql("SELECT * FROM bi_schema.regions", engine)

df = df.merge(df_infos, on=["titre", "lien"], how="left")
df = df.merge(df_regions, on="ville", how="left")

df_fact = df[["titre_id", "ville_id", "prix", "surface", "chambres", "salle_de_bain", "prix_m2"]]
df_fact.to_sql("fact_avito", engine, if_exists="append", schema="bi_schema", index=False)