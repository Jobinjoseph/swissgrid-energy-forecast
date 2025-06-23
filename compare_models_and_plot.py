# -*- coding: utf-8 -*-
"""
@author: joseph
"""

import matplotlib.pyplot as plt
import pandas as pd

def compare_models_plot(forecast_Prophet, forecast_neural, df):
    """
    Plots forecasted vs actual values for both Prophet and NeuralProphet.
    Also prints expected increase or decrease in consumption.
    """

    # Merge forecasts with actuals for consistent plotting
    if 'yhat1' in forecast_neural.columns and 'yhat' not in forecast_neural.columns:
        forecast_neural.rename(columns={'yhat1': 'yhat'}, inplace=True)
    df_actual = df[['ds', 'y']].drop_duplicates(subset='ds')
    forecast_Prophet = forecast_Prophet[['ds', 'yhat']].rename(columns={'yhat': 'yhat_prophet'})
    forecast_neural = forecast_neural[['ds', 'yhat']].rename(columns={'yhat': 'yhat_neural'})

    # Merge all
    df_plot = df_actual.merge(forecast_Prophet, on='ds', how='outer').merge(forecast_neural, on='ds', how='outer')
    df_plot = df_plot.sort_values('ds')

    # Plot
    plt.figure(figsize=(16, 6))
    if df_plot['y'].notna().sum() > 0:
        plt.plot(df_plot['ds'], df_plot['y'], label='Actual', linewidth=1.5, color='black')

    if df_plot['yhat_prophet'].notna().sum() > 0:
        plt.plot(df_plot['ds'], df_plot['yhat_prophet'], label='Prophet Forecast', linestyle='--', color='blue')

    if df_plot['yhat_neural'].notna().sum() > 0:
        plt.plot(df_plot['ds'], df_plot['yhat_neural'], label='NeuralProphet Forecast', linestyle='--', color='green')

    plt.title("Energy Load Forecast: Prophet vs NeuralProphet")
    plt.xlabel("Date")
    plt.ylabel("Load [MWh]")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Compare starting and ending forecast value
    try:
        last_actual = df_plot[df_plot['y'].notna()]['y'].iloc[-1]
        future_prophet = df_plot[df_plot['yhat_prophet'].notna() & df_plot['y'].isna()]
        end_prophet = future_prophet['yhat_prophet'].iloc[-1]

        trend = "increase" if end_prophet > last_actual else "decrease"
        percent_change = ((end_prophet - last_actual) / last_actual) * 100
        print(f"\n Based on Prophet, the load is expected to {trend} by {percent_change:.2f}% over the next 15 days.")
    except:
        print("Could not compute trend from Prophet (missing values).")
