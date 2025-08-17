import matplotlib.pyplot as plt
from xgboost import XGBRegressor
import numpy as np

def load_model(model_path):
    model = XGBRegressor()
    model.load_model(model_path)
    return model

def predict_day(df_day, model, feature_cols):
    df_day = df_day.dropna(subset=feature_cols).copy()
    df_day['predicted_spaces'] = model.predict(df_day[feature_cols])
    residuals = model.predict(df_day[feature_cols])
    return df_day

def recursive_predict(model, last_data, n_steps=1440):  # 1440 minutes = 1 day
    preds = []
    current_input = last_data.copy()

    for _ in range(n_steps):
        pred = model.predict(current_input.values.reshape(1, -1))[0]
        preds.append(pred)

        # Shift lag features
        lag_features = current_input.filter(like='lag_').values
        new_lags = np.roll(lag_features, shift=1)
        new_lags[0] = pred

        # Update the lag features with new predictions
        for i, name in enumerate(current_input.filter(like='lag_').index):
            current_input[name] = new_lags[i]

    return preds


def plot_actual_vs_predicted(df_day, carpark_code, date_str):
    plt.figure(figsize=(14, 6))
    plt.plot(df_day['time'], df_day['spaces'], label='Actual', color='blue', linewidth=2)
    plt.plot(df_day['time'], df_day['predicted_spaces'], label='Predicted', color='orange', linestyle='--', linewidth=2)
    plt.title(f"Car Park {carpark_code} – Actual vs Predicted Spaces on {date_str}")
    plt.xlabel("Time")
    plt.ylabel("Spaces Available")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
