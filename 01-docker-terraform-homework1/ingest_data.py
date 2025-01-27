#!/usr/bin/env python3

import argparse
import os
from time import time
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

    if url.endswith(".csv.gz"):
        csv_name = "output.csv.gz"
    else:
        csv_name = "output.csv"

    os.system(f"wget {url} -O {csv_name}")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, dtype={"store_and_fwd_flag":str})
    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
    df.to_sql(name=table_name, con=engine, if_exists="append")
    print("Creating heading for the table")
    
    while True:
        try:
            t_start = time()
            df = next(df_iter)
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df.to_sql(name=table_name, con=engine, if_exists="append")
            t_end = time()
            print("Inserted another chunk, took %.3f second" % (t_end - t_start))
        except StopIteration:
            print("Finished ingesting data into postgres database")
            break
    #adding taxi_zone table
    print("Adding taxing_zone table")
    t_start = time()
    os.system("wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv -O taxi_zone")
    df_tz = pd.read_csv("taxi_zone")
    df_tz.head(n=0).to_sql(name="taxi_zone_lookup", con=engine, if_exists="replace")
    df_tz.to_sql(name="taxi_zone_lookup", con=engine, if_exists="append")
    t_end = time()
    print("Taxi zone added %.3f" % (t_end - t_start))

if __name__ == "__main__":
    #creata parser
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")
    parser.add_argument("--user", required=True, help = "user name for postgres")
    parser.add_argument("--password", required=True, help = "password for postgres")
    parser.add_argument("--host", required=True, help = "host for postgres")
    parser.add_argument("--port", required=True, help = "port for postgres")
    parser.add_argument("--db", required=True, help = "db name for postgres")
    parser.add_argument("--table_name", required=True, help = "table name of database")
    parser.add_argument("--url", required=True, help = "url for the csv file")
    #parse argument
    args = parser.parse_args()
    #execute main function with parameter
    main(args)
