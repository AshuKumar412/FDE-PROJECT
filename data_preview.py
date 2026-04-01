
import pandas as pd
import os
from pathlib import Path

def preview_data():
    """Preview all CSV files"""
    data_path = Path(r"C:\FED-PROJECT\Project dataset\data")
    
    print("\n" + "="*70)
    print("📊 DATA PREVIEW")
    print("="*70)
    
    files = ['appointments.csv', 'billing.csv', 'doctors.csv', 'patients.csv', 'treatments.csv']
    
    for file in files:
        file_path = data_path / file
        if file_path.exists():
            df = pd.read_csv(file_path)
            print(f"\n📁 {file}:")
            print(f"   Shape: {df.shape}")
            print(f"   Columns: {list(df.columns)}")
            print(f"   First 3 rows:")
            print(df.head(3))
            print("-"*50)
        else:
            print(f"\n❌ {file} not found at {file_path}")

if __name__ == "__main__":
    preview_data()