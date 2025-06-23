# -*- coding: utf-8 -*-
"""
@author: joseph
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

def calculate_rmse(y_true, y_pred):
    """
    Root Mean Squared Error
    """
    return np.sqrt(mean_squared_error(y_true, y_pred))

def calculate_mape(y_true, y_pred):
    """
    Mean Absolute Percentage Error
    """
    return mean_absolute_percentage_error(y_true, y_pred) * 100

def evaluate_forecast(df_actual, df_forecast, metric_functions=None):
    """
    Evaluate forecast by comparing actual vs predicted values.

    :param df_actual: DataFrame with ['ds', 'y'] — actual values
    :param df_forecast: DataFrame with ['ds', 'yhat'] — forecast values
    :param metric_functions: List of functions to evaluate (e.g., [calculate_rmse, calculate_mape])
    :return: dict of metric results
    """
    print("df_actual type:", type(df_actual))
    print("df_forecast type:", type(df_forecast))
    if metric_functions is None:
        metric_functions = [calculate_rmse, calculate_mape]

    # Merge on timestamp
    df_merged = pd.merge(df_actual[['ds', 'y']], df_forecast[['ds', 'yhat']], on='ds', how='inner')

    # Filter out rows with NaNs in 'y' or 'yhat'
    df_merged = df_merged.dropna(subset=['y', 'yhat'])
    
    if df_merged.empty:
        raise ValueError("Merged dataframe is empty after dropping NaNs. Check forecast and actual alignment.")


    results = {}
    for func in metric_functions:
        name = func.__name__.replace('calculate_', '').upper()
        results[name] = func(df_merged['y'], df_merged['yhat'])

    return results
