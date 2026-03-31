"""
Data Transformation Module
Cleans, merges, and prepares data for analysis
"""
import pandas as pd
import numpy as np
from datetime import datetime

def merge_data(appointments, billing, doctors, patients, treatments):
    """Merge all datasets into a single dataframe"""
    print("\n🔄 MERGING DATA...")
    
    # Start with appointments as base
    if appointments is not None:
        merged = appointments.copy()
        print(f"   Base appointments shape: {merged.shape}")
    else:
        merged = None
        return None
    
    # Merge with patients first (so we have patient info)
    if patients is not None and merged is not None:
        if 'patient_id' in patients.columns and 'patient_id' in merged.columns:
            patient_cols = [col for col in patients.columns if col != 'patient_id']
            patients_subset = patients[['patient_id'] + patient_cols]
            merged = pd.merge(merged, patients_subset, on='patient_id', how='left')
            print(f"   ✓ Merged with patient data - new shape: {merged.shape}")
    
    # Merge with billing using patient_id - avoid duplicates by dropping duplicates first
    if billing is not None and merged is not None:
        if 'patient_id' in billing.columns and 'patient_id' in merged.columns:
            # Drop duplicate patient_id in billing to avoid multiple matches
            billing_unique = billing.drop_duplicates(subset=['patient_id'], keep='first')
            
            # Keep only relevant billing columns
            billing_cols = ['patient_id', 'amount', 'payment_status', 'payment_method', 'bill_date']
            billing_cols = [col for col in billing_cols if col in billing_unique.columns]
            billing_subset = billing_unique[billing_cols]
            
            merged = pd.merge(merged, billing_subset, on='patient_id', how='left', suffixes=('', '_bill'))
            print(f"   ✓ Merged with billing data using patient_id")
            print(f"   ✓ New shape: {merged.shape}")
            
            # Check if amount column exists after merge
            if 'amount' in merged.columns:
                print(f"   ✓ Amount column found with total: ${merged['amount'].sum():,.2f}")
                print(f"   ✓ Amount range: ${merged['amount'].min():,.2f} - ${merged['amount'].max():,.2f}")
            else:
                print(f"   ⚠️ Amount column not found after merge")
        else:
            print(f"   ⚠️ Cannot merge billing - patient_id missing in billing")
    
    # Merge with doctors
    if doctors is not None and merged is not None:
        if 'doctor_id' in doctors.columns and 'doctor_id' in merged.columns:
            doctor_cols = [col for col in doctors.columns if col != 'doctor_id']
            doctors_subset = doctors[['doctor_id'] + doctor_cols]
            merged = pd.merge(merged, doctors_subset, on='doctor_id', how='left')
            print(f"   ✓ Merged with doctor data - new shape: {merged.shape}")
    
    # Merge with treatments (if treatment_id exists in appointments)
    if treatments is not None and merged is not None:
        if 'treatment_id' in treatments.columns and 'treatment_id' in merged.columns:
            treatment_cols = [col for col in treatments.columns if col != 'treatment_id']
            treatments_subset = treatments[['treatment_id'] + treatment_cols]
            merged = pd.merge(merged, treatments_subset, on='treatment_id', how='left')
            print(f"   ✓ Merged with treatment data - new shape: {merged.shape}")
        else:
            print(f"   ℹ️ Skipping treatment merge - treatment_id not available in appointments")
    
    return merged

def add_derived_columns(df):
    """Add calculated columns for analysis"""
    print("\n📊 ADDING DERIVED COLUMNS...")
    
    # Add month column if date exists
    date_columns = ['appointment_date', 'date', 'created_at', 'bill_date']
    for col in date_columns:
        if col in df.columns:
            try:
                df['Month'] = pd.to_datetime(df[col]).dt.strftime('%Y-%m')
                print(f"   ✓ Added Month column from {col}")
                break
            except:
                continue
    
    # Add age if birth date exists
    if 'date_of_birth' in df.columns:
        try:
            df['Age'] = pd.to_datetime('today').year - pd.to_datetime(df['date_of_birth']).dt.year
            print("   ✓ Added Age column")
        except:
            pass
    
    # Add cost categories
    if 'amount' in df.columns:
        df['cost_category'] = pd.cut(
            df['amount'],
            bins=[0, 100, 500, 1000, 5000, float('inf')],
            labels=['Low', 'Medium', 'High', 'Very High', 'Premium']
        )
        print("   ✓ Added cost categories")
    
    # Add day of week
    date_columns = ['appointment_date', 'date', 'created_at', 'bill_date']
    for col in date_columns:
        if col in df.columns:
            try:
                df['day_of_week'] = pd.to_datetime(df[col]).dt.day_name()
                print("   ✓ Added day of week column")
                break
            except:
                continue
    
    # Add season
    date_columns = ['appointment_date', 'date', 'created_at', 'bill_date']
    for col in date_columns:
        if col in df.columns:
            try:
                month = pd.to_datetime(df[col]).dt.month
                df['season'] = month.map({
                    12: 'Winter', 1: 'Winter', 2: 'Winter',
                    3: 'Spring', 4: 'Spring', 5: 'Spring',
                    6: 'Summer', 7: 'Summer', 8: 'Summer',
                    9: 'Fall', 10: 'Fall', 11: 'Fall'
                })
                print("   ✓ Added season column")
                break
            except:
                continue
    
    return df

def clean_data(df):
    """Clean the merged dataframe"""
    print("\n🧹 CLEANING DATA...")
    
    # Remove duplicates
    initial_count = len(df)
    df = df.drop_duplicates()
    removed = initial_count - len(df)
    if removed > 0:
        print(f"   ✓ Removed {removed} duplicate records")
    
    # Handle missing values - Fixed for categorical columns
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].fillna(0)
        elif pd.api.types.is_categorical_dtype(df[col]):
            # For categorical columns, add 'Unknown' as a category first
            if 'Unknown' not in df[col].cat.categories:
                df[col] = df[col].cat.add_categories(['Unknown'])
            df[col] = df[col].fillna('Unknown')
        else:
            df[col] = df[col].fillna('Unknown')
    print("   ✓ Handled missing values")
    
    # Remove outliers (for numeric columns)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        try:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        except:
            pass
    print("   ✓ Removed outliers")
    
    return df

def get_insights(df):
    """Generate insights from the data"""
    insights = {}
    
    insights['total_records'] = len(df)
    
    if 'patient_id' in df.columns:
        insights['total_patients'] = df['patient_id'].nunique()
    
    if 'doctor_id' in df.columns:
        insights['total_doctors'] = df['doctor_id'].nunique()
    elif 'doctor_name' in df.columns:
        insights['total_doctors'] = df['doctor_name'].nunique()
    
    if 'amount' in df.columns:
        insights['total_revenue'] = df['amount'].sum()
        insights['avg_cost'] = df['amount'].mean()
        insights['median_cost'] = df['amount'].median()
        insights['min_cost'] = df['amount'].min()
        insights['max_cost'] = df['amount'].max()
    else:
        insights['total_revenue'] = 0
        insights['avg_cost'] = 0
    
    if 'treatment_type' in df.columns:
        insights['treatment_counts'] = df['treatment_type'].value_counts().to_dict()
        insights['most_common_treatment'] = df['treatment_type'].mode()[0] if len(df['treatment_type'].mode()) > 0 else None
    
    # Doctor revenue
    if 'amount' in df.columns:
        doctor_col = None
        for col in df.columns:
            if 'doctor' in col.lower() and ('name' in col.lower() or 'first_name' in col.lower()):
                doctor_col = col
                break
        if not doctor_col and 'first_name' in df.columns and 'last_name' in df.columns:
            df['doctor_name'] = df['first_name'] + ' ' + df['last_name']
            doctor_col = 'doctor_name'
        
        if doctor_col:
            insights['doctor_revenue'] = df.groupby(doctor_col)['amount'].sum().sort_values(ascending=False).to_dict()
    
    # Status counts
    if 'status' in df.columns:
        insights['status_counts'] = df['status'].value_counts().to_dict()
    
    if 'payment_status' in df.columns:
        insights['payment_status_counts'] = df['payment_status'].value_counts().to_dict()
    
    # Age statistics
    if 'Age' in df.columns:
        insights['avg_age'] = df['Age'].mean()
        insights['age_range'] = (df['Age'].min(), df['Age'].max())
    
    # Gender distribution
    if 'gender' in df.columns:
        insights['gender_counts'] = df['gender'].value_counts().to_dict()
    
    # Monthly trends
    if 'Month' in df.columns and 'amount' in df.columns:
        insights['monthly_revenue'] = df.groupby('Month')['amount'].sum().to_dict()
        insights['monthly_visits'] = df.groupby('Month').size().to_dict()
    
    return insights

def transform_all_data(raw_data):
    """Transform all extracted data"""
    print("\n" + "="*50)
    print("🔄 TRANSFORMING DATA")
    print("="*50)
    
    # Extract individual datasets
    appointments = raw_data.get('appointments')
    billing = raw_data.get('billing')
    doctors = raw_data.get('doctors')
    patients = raw_data.get('patients')
    treatments = raw_data.get('treatments')
    
    # Merge all data
    merged_df = merge_data(appointments, billing, doctors, patients, treatments)
    
    if merged_df is None or len(merged_df) == 0:
        print("❌ No data to transform")
        return None, None
    
    # Add derived columns
    merged_df = add_derived_columns(merged_df)
    
    # Clean data
    merged_df = clean_data(merged_df)
    
    # Generate insights
    insights = get_insights(merged_df)
    
    print("\n✅ Transformation complete!")
    print(f"   Final dataset shape: {merged_df.shape}")
    
    return merged_df, insights