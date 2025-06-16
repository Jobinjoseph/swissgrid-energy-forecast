# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 11:14:52 2025

@author: joseph
"""
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

BASE_URL = "https://www.swissgrid.ch/en/home/operation/grid-data/generation.html"
DOWNLOAD_FOLDER = "data"

def fetch_latest_excel():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(BASE_URL, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")

    excel_links = soup.find_all("a", href=True)
    excel_files = [urljoin(BASE_URL, link['href']) for link in excel_links if link['href'].endswith(".xlsx")]

    if not excel_files:
        return None

    latest_file_url = excel_files[0]
    filename = os.path.basename(latest_file_url)
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        print(f"Downloading {filename}")
        file_r = requests.get(latest_file_url, headers=headers)
        with open(filepath, "wb") as f:
            f.write(file_r.content)
        return filepath
    else:
        print(f"File {filename} already exists.")
        return filepath

