
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from pipeline import extract_all_data, transform_all_data, load_to_database
# import time

# def print_progress(message, step=0, total=3):
#     """Print progress with animation"""
#     bar_length = 40
#     progress = step / total
#     filled_length = int(bar_length * progress)
#     bar = '█' * filled_length + '░' * (bar_length - filled_length)
#     print(f"\r[{bar}] {progress*100:.0f}% - {message}", end='')
#     if step == total:
#         print()

# def main():
#     """Run complete pipeline"""
#     print("\n" + "="*70)
#     print("🏥 HEALTHCARE DATA PIPELINE")
#     print("="*70)
    
#     # Step 1: Extract
#     print_progress("Extracting data...", 1, 3)
#     raw_data = extract_all_data()
    
#     # Check if we have any data
#     has_data = False
#     for key, value in raw_data.items():
#         if value is not None and len(value) > 0:
#             has_data = True
#             break
    
#     if not has_data:
#         print("\n❌ No data found. Please place CSV files in C:\\FED-PROJECT\\Project dataset\\data\\")
#         return
    
#     # Step 2: Transform
#     print_progress("Transforming data...", 2, 3)
#     transformed_data, insights = transform_all_data(raw_data)
    
#     if transformed_data is None or len(transformed_data) == 0:
#         print("\n❌ Transformation failed")
#         return
    
#     # Step 3: Load
#     print_progress("Loading to database...", 3, 3)
#     success = load_to_database(transformed_data)
    
#     print_progress("Pipeline complete!", 3, 3)
#     print()
    
#     if success:
#         print("\n" + "="*70)
#         print("✅ PIPELINE EXECUTED SUCCESSFULLY!")
#         print("="*70)
        
#         print("\n📊 SUMMARY STATISTICS:")
#         if insights:
#             print(f"   • Total Records: {insights.get('total_records', 0):,}")
#             print(f"   • Total Patients: {insights.get('total_patients', 0):,}")
#             print(f"   • Total Doctors: {insights.get('total_doctors', 0):,}")
#             print(f"   • Total Revenue: ${insights.get('total_revenue', 0):,.2f}")
#             print(f"   • Average Cost: ${insights.get('avg_cost', 0):,.2f}")
        
#         if insights and insights.get('doctor_revenue'):
#             print("\n🏆 TOP PERFORMERS:")
#             for i, (doctor, revenue) in enumerate(list(insights.get('doctor_revenue', {}).items())[:5], 1):
#                 print(f"   {i}. {doctor}: ${revenue:,.2f}")
        
#         print("\n🎯 NEXT STEPS:")
#         print("   1. Launch dashboard: cd dashboard && streamlit run app.py")
#         print("   2. Explore interactive visualizations")
#         print("   3. Apply filters to analyze specific segments")

# if __name__ == "__main__":
#     main()






import sys
import os
import time

# Fix path for both local + Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from pipeline import extract_all_data, transform_all_data, load_to_database

def print_progress(message, step=0, total=3):
    """Print progress bar"""
    bar_length = 40
    progress = step / total
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f"\r[{bar}] {progress*100:.0f}% - {message}", end='')
    if step == total:
        print()

def check_data_exists():
    """Check if CSV files exist (important for deployment)"""
    data_path = os.path.join(BASE_DIR, "data")
    
    required_files = [
        "patients.csv",
        "doctors.csv",
        "appointments.csv",
        "treatments.csv",
        "billing.csv"
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(os.path.join(data_path, file)):
            missing.append(file)
    
    if missing:
        print("\n❌ Missing dataset files:")
        for f in missing:
            print(f"   - {f}")
        print("\n📂 Make sure CSV files are inside 'data/' folder")
        return False
    
    print("\n✅ All required dataset files found:")
    for file in required_files:
        file_path = os.path.join(data_path, file)
        file_size = os.path.getsize(file_path) / 1024  # Size in KB
        print(f"   • {file}: {file_size:.1f} KB")
    
    return True

def get_data_stats(dataframes):
    """Get basic stats from dataframes"""
    stats = {}
    for name, df in dataframes.items():
        if df is not None:
            stats[name] = {
                'rows': len(df),
                'columns': len(df.columns)
            }
    return stats

def main():
    print("\n" + "=" * 70)
    print("🏥 HEALTHCARE DATA PIPELINE")
    print("=" * 70)
    
    # Check dataset exists
    if not check_data_exists():
        print("\n⚠️ Please place your CSV files in the 'data/' folder and try again.")
        return
    
    # Step 1: Extract
    print_progress("Extracting data...", 1, 3)
    raw_data = extract_all_data()
    
    # Check if any data was extracted
    has_data = any(value is not None and len(value) > 0 for value in raw_data.values())
    
    if not has_data:
        print("\n❌ No data found in CSV files")
        print("\n💡 Troubleshooting:")
        print("   • Check if CSV files are readable")
        print("   • Verify column names match expected format")
        print("   • Ensure files are not empty")
        return
    
    # Show extraction summary
    print("\n📊 Extraction Summary:")
    stats = get_data_stats(raw_data)
    for name, stat in stats.items():
        print(f"   • {name.capitalize()}: {stat['rows']:,} rows, {stat['columns']} columns")
    
    # Step 2: Transform
    print_progress("Transforming data...", 2, 3)
    try:
        transformed_data, insights = transform_all_data(raw_data)
    except Exception as e:
        print(f"\n❌ Transformation error: {e}")
        return
    
    if transformed_data is None or len(transformed_data) == 0:
        print("\n❌ Transformation failed - no data produced")
        return
    
    print(f"\n📊 Transformation Summary:")
    print(f"   • Final records: {len(transformed_data):,}")
    print(f"   • Features created: {len(transformed_data.columns)}")
    
    # Step 3: Load
    print_progress("Loading to database...", 3, 3)
    try:
        success = load_to_database(transformed_data)
    except Exception as e:
        print(f"\n❌ Loading error: {e}")
        return
    
    print_progress("Pipeline complete!", 3, 3)
    print()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ PIPELINE EXECUTED SUCCESSFULLY!")
        print("=" * 70)
        
        print("\n📊 SUMMARY STATISTICS:")
        if insights:
            print(f"   • Total Records: {insights.get('total_records', len(transformed_data)):,}")
            print(f"   • Total Patients: {insights.get('total_patients', 0):,}")
            print(f"   • Total Doctors: {insights.get('total_doctors', 0):,}")
            print(f"   • Total Revenue: ${insights.get('total_revenue', 0):,.2f}")
            print(f"   • Average Cost: ${insights.get('avg_cost', 0):,.2f}")
            
            # Additional insights if available
            if 'most_common_treatment' in insights:
                print(f"   • Most Common Treatment: {insights['most_common_treatment']}")
            if 'completion_rate' in insights:
                print(f"   • Completion Rate: {insights['completion_rate']:.1f}%")
        
        print("\n🎯 NEXT STEPS:")
        print("   1. Launch dashboard:")
        print("      cd dashboard")
        print("      streamlit run app.py")
        print("\n   2. Or run directly:")
        print("      streamlit run dashboard/app.py")
        
        # Show database location
        db_path = os.path.join(BASE_DIR, "database", "healthcare.db")
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path) / (1024 * 1024)  # Size in MB
            print(f"\n💾 Database created: {db_path}")
            print(f"   Database size: {db_size:.2f} MB")
    
    else:
        print("\n❌ Pipeline failed during loading stage")
        print("💡 Check if database directory is writable")

if __name__ == "__main__":
    main()