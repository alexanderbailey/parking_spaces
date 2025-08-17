import os
import pandas as pd
from sqlalchemy import create_engine
from parks_models.config import cache_dir, db_url, cache_format

os.makedirs(cache_dir, exist_ok=True)

def get_engine():
    return create_engine(db_url)

def query_carpark_codes():
    engine = get_engine()
    with engine.connect() as conn:
        df_carpark_codes = pd.read_sql("SELECT code FROM carpark", conn)
    return df_carpark_codes

def query_carpark_spaces(carpark_code):
    engine = get_engine()
    query = f"""
        SELECT
            c.code as carpark_code,
            s.open,
            s.spaces,
            s.unusable_spaces,
            s.time
        FROM spaces s
        LEFT JOIN carpark c ON s.carpark_id = c.id
        WHERE c.code = '{carpark_code}'
    """
    with engine.connect() as conn:
        df_spaces = pd.read_sql(query, conn)
    return df_spaces

def load_carpark_spaces(carpark_code, force_refresh):
    # Check if cached file exists
    file_path = os.path.join(cache_dir, f"{carpark_code}.parquet")
    
    if not force_refresh and os.path.exists(file_path):
        print(f"📂 Using cached data for {carpark_code}")
        df_spaces = pd.read_parquet(file_path)
    else:
        print(f"🛰️  Fetching from DB for {carpark_code}")
        df_spaces = query_carpark_spaces(carpark_code)

        # Save to Parquet
        df_spaces.to_parquet(file_path, index=False)

    return df_spaces


def load_all_data(force_refresh=False):
    # Load carpark codes
    df_carparks = query_carpark_codes()
    dfs = []
    for _, row in df_carparks.iterrows():
        df_spaces = load_carpark_spaces(
            carpark_code=row['code'],
            force_refresh=force_refresh
        )
        dfs.append(df_spaces)

    df = pd.concat(dfs, ignore_index=True)
    return df
