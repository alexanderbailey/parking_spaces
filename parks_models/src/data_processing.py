import pandas as pd
from uuid import UUID

# def add_baseline(df):
#     df['hour_of_week'] = df['dayofweek'] * 24 + df['hour']

#     # Compute average spaces per hour-of-week per carpark
#     baseline = df.groupby(['carpark_code', 'hour_of_week'])['spaces'].mean().reset_index()
#     baseline = baseline.rename(columns={'spaces': 'baseline_spaces'})

#     # Merge back into the main dataframe
#     df = df.merge(baseline, on=['carpark_code', 'hour_of_week'], how='left')

#     # Compute residuals
#     df['residual'] = df['spaces'] - df['baseline_spaces']

#     return df


def preprocess_data(df, lags=10):
    # Convert to datetime
    df['time'] = pd.to_datetime(df['time'], utc=True).dt.tz_convert(None)
    # Sort
    df = df.sort_values(['carpark_code', 'time'])

    # Extract features
    df['minute'] = df['time'].dt.minute
    df['hour'] = df['time'].dt.hour
    df['dayofweek'] = df['time'].dt.dayofweek
    df['month'] = df['time'].dt.month
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)

    # Lag features
    df['prev_spaces'] = df.groupby('carpark_code')['spaces'].shift(1)

    # df = add_baseline(df)

    # Create lag features
    for lag in range(1, lags + 1):
        df[f'lag_{lag}'] = df.groupby('carpark_code')['spaces'].shift(lag)

    # Remove any rows where lag features are missing
    df = df.dropna(subset=[f'lag_{lag}' for lag in range(1, lags + 1)])

    return df

def get_day_for_carpark(df, carpark_code, date_str):
    date = pd.to_datetime(date_str)
    prev_day = date - pd.Timedelta(days=1)
    next_day = date + pd.Timedelta(days=1)

    df_filtered = df[
        (df['carpark_code'] == carpark_code) &
        (df['time'] >= prev_day) &
        (df['time'] < next_day)
    ].copy()

    df_filtered = preprocess_data(df_filtered)

    df_day = df_filtered[
        (df_filtered['time'] >= date) &
        (df_filtered['time'] < next_day)
    ].copy()

    return df_day
