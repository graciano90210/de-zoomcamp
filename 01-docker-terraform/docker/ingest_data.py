import argparse

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}")

    df_iter = pd.read_csv(url, compression="gzip", iterator=True, chunksize=100000)

    first_chunk = True

    for df in df_iter:
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        if first_chunk:
            df.to_sql(name=table_name, con=engine, if_exists="replace")
            first_chunk = False
        else:
            df.to_sql(name=table_name, con=engine, if_exists="append")

        print(f"Insertado un bloque de {len(df)} filas")

    print("Datos cargados en Postgres")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingesta de datos de taxis NYC a Postgres")

    parser.add_argument("--user", help="usuario de la base de datos")
    parser.add_argument("--password", help="contraseña de la base de datos")
    parser.add_argument("--host", help="host del servidor de la base de datos")
    parser.add_argument("--port", help="puerto del servidor de la base de datos")
    parser.add_argument("--db", help="nombre de la base de datos")
    parser.add_argument("--table_name", help="nombre de la tabla destino")
    parser.add_argument("--url", help="url del archivo csv a descargar")

    args = parser.parse_args()

    main(args)
