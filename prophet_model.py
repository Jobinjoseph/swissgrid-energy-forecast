# -*- coding: utf-8 -*-
"""
@author: joseph
"""

# models/prophet_model.py

import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os

def train_prophet(df, forecast_days=14):
    """
    Trains a Prophet model and forecasts into the future.
    
    Parameters:
    - df: pandas DataFrame with columns 'ds' (datetime) and 'y' (target).
    - forecast_days: Number of days to forecast into the future.

    Returns:
    - forecast: Prophet forecast DataFrame.
    - model: trained Prophet model object.
    """
    model = Prophet(daily_seasonality=True, weekly_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=forecast_days * 96, freq="15min")  # 96 = 15-min intervals per day
    forecast_Prophet = model.predict(future)

    forecast_Prophet['model'] = 'Prophet'
    return forecast_Prophet, model


def plot_forecast(model, forecast_Prophet, output_path=None):
    """
    Plots forecast from a trained Prophet model.

    Parameters:
    - model: Trained Prophet model object.
    - forecast: Forecast DataFrame from Prophet.
    - output_path: (Optional) File path to save the plot.
    """
    fig = model.plot(forecast_Prophet)
    plt.title("Prophet Forecast")
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fig.savefig(output_path)
    plt.show()
