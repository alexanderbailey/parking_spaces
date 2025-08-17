import ray
import os
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def init_ray():
    ray.init(num_gpus=1, ignore_reinit_error=True)

@ray.remote(num_gpus=1)
def train_model_for_carpark(carpark_code, group, feature_cols):
    group = group.dropna(subset=feature_cols + ['spaces']).copy()
    if len(group) < 50:
        return carpark_code, None, None

    X = group[feature_cols]
    y = group['spaces']
    # y = group['residual']  # Use residuals for training

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False,  #random_state=42
    )

    model = XGBRegressor(
        tree_method='gpu_hist',
        predictor='gpu_predictor',
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    os.makedirs("models", exist_ok=True)
    model_filename = f"models/{carpark_code}.json"
    model.save_model(model_filename)

    return carpark_code, model_filename, mae

def train_all_models(df, feature_cols):
    grouped = df.groupby('carpark_code')

    futures = []
    for carpark_code, group in grouped:
        futures.append(train_model_for_carpark.remote(carpark_code, group, feature_cols))

    results = ray.get(futures)

    metrics_by_carpark = {}
    for carpark_code, model_path, mae in results:
        if mae is not None:
            print(f"✅ Carpark {carpark_code} — Model saved at {model_path} — MAE: {mae:.2f}")
            metrics_by_carpark[carpark_code] = mae
        else:
            print(f"⚠️ Carpark {carpark_code} skipped (not enough data)")

    return metrics_by_carpark
