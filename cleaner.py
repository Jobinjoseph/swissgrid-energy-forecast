# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 11:15:47 2025

@author: joseph
"""

import pandas as pd
import os

def load_and_clean_excel(filepath):
    # Read Excel and skip 2nd row (units)
    df = pd.read_excel(filepath, skiprows=[1])

    # Remove trailing whitespaces or newline in columns
    df.columns = df.columns.str.strip()

    # Rename important columns
    df = df.rename(columns={
        df.columns[0]: 'ds',
        'Verbrauch Regelzone CH - Ausländische Gebiete\nConsumption control area CH - foreign territories': 'y'
    })

    # Convert time to datetime
    df['ds'] = pd.to_datetime(df['ds'], format='%d.%m.%Y %H:%M', errors='coerce')

    # Convert energy to numeric (kWh → MWh)
    df['y'] = pd.to_numeric(df['y'], errors='coerce') / 1000.0

    # Clean
    df = df.dropna(subset=['ds', 'y'])
    df = df.drop_duplicates(subset=['ds'])
    df = df.sort_values('ds')

    return df
