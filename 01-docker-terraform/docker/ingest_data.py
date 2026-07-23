import pandas as pd
from sqlalchemy import create_engine

url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

df = pd.read_csv(url, compression="gzip")

print(len(df))
print(df.head())

df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

engine = create_engine("postgresql+psycopg://root:root@localhost:5432/ny_taxi")

df.to_sql(name="ny_taxi_data", con=engine, if_exists="replace")

print("Datos cargados en Postgres")
