
import pandas as pd
import os
from pathlib import Path

def get_data_path():
    """Get the data directory path - points to your Project dataset folder"""
    # This points to C:\FED-PROJECT\Project dataset\data\
    base_path = Path(r"C:\FED-PROJECT\Project dataset")
    data_path = base_path / 'data'
    
    # If data folder doesn't exist, try the current directory
    if not data_path.exists():
        data_path = Path(__file__).parent.parent / 'data'
    
    return data_path

def extract_appointments():
    """Extract appointments data"""
    try:
        data_path = get_data_path() / 'appointments.csv'
        if data_path.exists():
            df = pd.read_csv(data_path)
            print(f"✅ Loaded {len(df)} appointment records")
            return df
        else:
            print(f"⚠️ File not found: {data_path}")
            return None
    except Exception as e:
        print(f"❌ Error loading appointments: {e}")
        return None

def extract_billing():
    """Extract billing data"""
    try:
        data_path = get_data_path() / 'billing.csv'
        if data_path.exists():
            df = pd.read_csv(data_path)
            # Ensure amount is numeric
            if 'amount' in df.columns:
                df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
                print(f"✅ Loaded {len(df)} billing records")
                print(f"   Total amount: ${df['amount'].sum():,.2f}")
                print(f"   Average amount: ${df['amount'].mean():,.2f}")
            else:
                print(f"✅ Loaded {len(df)} billing records (no amount column)")
            return df
        else:
            print(f"⚠️ File not found: {data_path}")
            return None
    except Exception as e:
        print(f"❌ Error loading billing: {e}")
        return None

def extract_doctors():
    """Extract doctors data"""
    try:
        data_path = get_data_path() / 'doctors.csv'
        if data_path.exists():
            df = pd.read_csv(data_path)
            print(f"✅ Loaded {len(df)} doctor records")
            return df
        else:
            print(f"⚠️ File not found: {data_path}")
            return None
    except Exception as e:
        print(f"❌ Error loading doctors: {e}")
        return None

def extract_patients():
    """Extract patients data"""
    try:
        data_path = get_data_path() / 'patients.csv'
        if data_path.exists():
            df = pd.read_csv(data_path)
            print(f"✅ Loaded {len(df)} patient records")
            return df
        else:
            print(f"⚠️ File not found: {data_path}")
            return None
    except Exception as e:
        print(f"❌ Error loading patients: {e}")
        return None

def extract_treatments():
    """Extract treatments data"""
    try:
        data_path = get_data_path() / 'treatments.csv'
        if data_path.exists():
            df = pd.read_csv(data_path)
            print(f"✅ Loaded {len(df)} treatment records")
            return df
        else:
            print(f"⚠️ File not found: {data_path}")
            return None
    except Exception as e:
        print(f"❌ Error loading treatments: {e}")
        return None

def extract_all_data():
    """Extract all data files"""
    print("\n📂 EXTRACTING DATA...")
    print("-" * 40)
    
    data = {
        'appointments': extract_appointments(),
        'billing': extract_billing(),
        'doctors': extract_doctors(),
        'patients': extract_patients(),
        'treatments': extract_treatments()
    }
    
    # Filter out None values
    data = {k: v for k, v in data.items() if v is not None}
    
    print(f"\n📊 Extracted {len(data)} datasets")
    return data