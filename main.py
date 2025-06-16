
from fetch_latest_data import download_latest_excel
from load_and_clean_data import load_and_clean_data
from prophet_model import train_prophet
from neuralprophet_model import train_neuralprophet_model
from compare_models_and_plot import compare_models_plot  # ✅ NEW
import os
import glob

# 💾 Define paths
DATA_DIR = r"xxxxx\data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
DATABASE_PATH = "database/forecast_results.db"
folder_path = RAW_DIR

# 📂 Find the Excel file manually if not downloaded
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))
if not excel_files:
    raise FileNotFoundError(f"No Excel file found in folder: {folder_path}")
file_path = excel_files[0]

def main():
    print("🔄 Step 1: Checking and downloading latest file...")
    excel_path = download_latest_excel(RAW_DIR)
    
    if not excel_path:
        # Fallback to most recent file
        files = sorted([f for f in os.listdir(RAW_DIR) if f.endswith('.xlsx')])
        if not files:
            raise FileNotFoundError("⚠️ No Excel file found to proceed.")
        excel_path = os.path.join(RAW_DIR, files[-1])
    
    print("🧹 Step 2: Loading and cleaning data...")
    df = load_and_clean_data(file_path)
    print(f"✅ Loaded dataframe with shape: {df.shape}")
    
    print("📈 Step 3: Running Prophet model...")
    forecast_Prophet, _ = train_prophet(df)

    print("🧠 Step 4: Running NeuralProphet model...")
    forecast_neural, _ = train_neuralprophet_model(df)
    
    print("📊 Step 5: Comparing model forecasts and visualizing results...")
    if 'yhat1' in forecast_neural.columns and 'yhat' not in forecast_neural.columns:
        forecast_neural.rename(columns={'yhat1': 'yhat'}, inplace=True)
    compare_models_plot(forecast_Prophet, forecast_neural, df)

    print("✅ All steps complete!")

if __name__ == "__main__":
    main()
