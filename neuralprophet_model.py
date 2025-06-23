# -*- coding: utf-8 -*-
"""
@author: joseph
"""

from neuralprophet import NeuralProphet
import matplotlib.pyplot as plt
def train_neuralprophet_model(df, forecast_periods=1440, plot_result=True):
   
    model = NeuralProphet(
        daily_seasonality=True,
        weekly_seasonality=True
    )

    # Fit the model on the full data
    model.fit(df, freq="15min")

    # Create future dataframe (includes training + forecast)
    future = model.make_future_dataframe(df, periods=forecast_periods)

    # Predict both historical and future values
    forecast_neural = model.predict(future)
    # Check how many rows have actual 'y' values
    print("Rows with actual values:", forecast_neural['y'].notna().sum())
    print("Rows with missing actual values:", forecast_neural['y'].isna().sum())
    
    # Show a few rows that *do* have actual values
    print("\nSample rows with actuals:")
    print(forecast_neural[forecast_neural['y'].notna()].head())
    
    # Show a few rows that are purely forecast (no actuals)
    print("\nSample forecast-only rows:")
    print(forecast_neural[forecast_neural['y'].isna()].head())


    # Add a column to identify the model
    forecast_neural['model_id'] = 'NeuralProphet'

    # Rename yhat1 to yhat for consistency
    forecast_neural.rename(columns={'yhat1': 'yhat'}, inplace=True)

    # PLOT if desired
    if plot_result:
        plt.figure(figsize=(15, 5))
        plt.plot(forecast_neural['ds'], forecast_neural['yhat'], label='Forecast_neural (yhat)', linestyle='--')
        
        # Only plot actuals where available (not NaNs)
        actual = forecast_neural.dropna(subset=['y'])
        plt.plot(actual['ds'], actual['y'], label='Actual (y)', alpha=0.6, color='orange')
    
        plt.title("NeuralProphet Forecast vs Actual")
        plt.xlabel("Time")
        plt.ylabel("Load (MWh)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    return forecast_neural, model
