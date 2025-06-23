# -*- coding: utf-8 -*-
"""
@author: joseph
"""
import os
import glob
import pandas as pd
import openpyxl
import xlwings as xw
folder_path = r"xxx\energy_forecast_project\data\raw"
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))
if not excel_files:
    raise FileNotFoundError(f"No Excel file found in folder: {folder_path}")
file_path = excel_files[0]


def load_and_clean_data(file_path):
    # Load workbook using xlwings
    app = xw.App(visible=False)
    book = xw.Book(file_path)
    sheet = book.sheets["Zeitreihen0h15"]
    data = sheet.range("A1").expand().value
    book.close()
    app.quit()

    # Combine the two header rows
    header_row_1 = data[0]
    header_row_2 = data[1]
    combined_headers = []
    for h1, h2 in zip(header_row_1, header_row_2):
        if h1 and h2:
            combined_headers.append(f"{h1.strip()} - {h2.strip()}")
        elif h2:
            combined_headers.append(h2.strip())
        elif h1:
            combined_headers.append(h1.strip())
        else:
            combined_headers.append("")

    # Create DataFrame
    df = pd.DataFrame(data[2:], columns=combined_headers)

    # Rename timestamp column to 'ds'
    timestamp_col = [col for col in df.columns if "Zeitstempel" in col or "timestamp" in col]
    if not timestamp_col:
        raise ValueError("Could not find a timestamp column.")
    df.rename(columns={timestamp_col[0]: "ds"}, inplace=True)

    # Parse datetime
    df["ds"] = pd.to_datetime(df["ds"], format="%d.%m.%Y %H:%M", errors="coerce")

    # Find consumption column
    target_col = [col for col in df.columns if "Verbrauch Regelzone CH - Ausländische Gebiete\nConsumption control area CH - foreign territories - kWh" in col or "Consumption control area CH" in col]
    if not target_col:
        print("Could not find expected consumption column.")
        print("Available columns:", df.columns[:10].tolist())
        raise ValueError("No usable consumption column found.")

    df.rename(columns={target_col[0]: "y"}, inplace=True)
    df = df[["ds", "y"]].dropna()

    # Convert kWh to MWh
    df["y"] = pd.to_numeric(df["y"], errors="coerce") / 1000.0
    df = df.dropna().drop_duplicates(subset="ds").sort_values("ds")

    return df
