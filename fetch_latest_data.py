import os
import time
import requests
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.swissgrid.ch"
TARGET_PAGE = "https://www.swissgrid.ch/en/home/operation/grid-data/generation.html#end-user-consumption"
download_folder = r"xxxx\energy_forecast_project\data\raw"
def download_latest_excel(download_folder):
    print("🌐 Opening browser to access Swissgrid download page...")

    options = Options()
    options.add_argument("--headless")  # Run in the background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Start Chrome with Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(TARGET_PAGE)
    
    print("⏳ Waiting for JavaScript content to load...")
    time.sleep(10)  # Give enough time for the page to fully render

    # Find all <a> tags
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"🔍 Total <a> links found: {len(links)}")

    # Extract and print all hrefs
    excel_links = []
    for link in links:
        href = link.get_attribute("href")
        if href:
            print("➡️ Found link:", href)
            if href.endswith(".xlsx"):
                excel_links.append(href)

    driver.quit()

    if not excel_links:
        print("❌ No Excel file link found.")
        return None

    # Use first Excel file link
    latest_url = excel_links[0]
    filename = os.path.basename(latest_url)
    local_path = os.path.join(download_folder, filename)

    if os.path.exists(local_path):
        print("✅ File already exists locally.")
        return local_path

    print(f"⬇️ Downloading Excel file from: {latest_url}")
    os.makedirs(download_folder, exist_ok=True)
    r = requests.get(latest_url)
    with open(local_path, "wb") as f:
        f.write(r.content)

    print(f"✅ Downloaded and saved as: {local_path}")
    return local_path
if __name__ == "__main__":
    download_latest_excel(download_folder)
