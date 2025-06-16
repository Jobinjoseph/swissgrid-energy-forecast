# ⚡ Swissgrid Energy Forecasting

This project downloads Swissgrid 15-minute energy consumption data and uses **Prophet** and **NeuralProphet** to forecast future consumption and visualize seasonality.

---

## 📦 Features

- 🔄 Automatically fetches the latest Excel data from [Swissgrid](https://www.swissgrid.ch/)
- 📈 Forecasts using [Facebook Prophet](https://facebook.github.io/prophet/) and [NeuralProphet](https://neuralprophet.com/)
- 📊 Visualizes forecasts and seasonal trends
- 💡 Indicates whether consumption is expected to rise or fall in the next 15 days

---

## 🛠 Installation

```bash
pip install -r requirements.txt

Run the Project
python main.py

📁 Folder Structure
main.py – orchestrates the pipeline

fetch_latest_data.py – downloads Swissgrid Excel file using Selenium

load_and_clean_data.py – parses and cleans the file using xlwings

prophet_model.py – forecasting with Prophet

neuralprophet_model.py – forecasting with NeuralProphet

compare_models_and_plot.py – compares both models visually

data/ – raw and processed data folders

Author
Jobin Joseph