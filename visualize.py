# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 11:34:43 2025

@author: joseph
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_forecast(forecast, model_name='Model'):
    """
    Plots the forecasted vs actual values.
    """
    plt.figure(figsize=(15, 6))
    if 'y' in forecast.columns:
        plt.plot(forecast['ds'], forecast['y'], label='Actual', linewidth=1.5)
    if 'yhat' in forecast.columns:
        plt.plot(forecast['ds'], forecast['yhat'], label='Forecast', linestyle='--')
    plt.title(f'Forecast vs Actual - {model_name}')
    plt.xlabel('Date')
    plt.ylabel('Load [MWh]')
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.show()

def compare_models(forecasts, metric_name='MAPE'):
    """
    Plots model comparison bar chart.
    Input: forecasts = list of dicts with keys: {'model': str, 'metric': float}
    """
    df = pd.DataFrame(forecasts)
    sns.barplot(data=df, x='model', y='metric')
    plt.title(f'Model Comparison - {metric_name}')
    plt.ylabel(metric_name)
    plt.xlabel('Model')
    plt.tight_layout()
    plt.grid(True, axis='y')
    plt.show()

def plot_seasonal_components(model, forecast, model_type='prophet'):
    """
    Plot seasonal components from a trained model.

    Args:
        model: trained model (Prophet or NeuralProphet object)
        forecast: DataFrame with forecasted results
        model_type: 'prophet' or 'neuralprophet'
    """
    if model_type == 'prophet':
        fig = model.plot_components(forecast)
        fig.suptitle("Seasonal Components - Prophet", fontsize=14)
        plt.tight_layout()
        plt.show()

    elif model_type == 'neuralprophet':
        fig = model.plot_components(forecast)
        plt.suptitle("Seasonal Components - NeuralProphet", fontsize=14)
        plt.tight_layout()
        plt.show()
