"""
Main Pipeline Orchestrator with Progress Tracking
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline import extract_all_data, transform_all_data, load_to_database
import time

def print_progress(message, step=0, total=3):
    """Print progress with animation"""
    bar_length = 40
    progress = step / total
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f"\r[{bar}] {progress*100:.0f}% - {message}", end='')
    if step == total:
        print()

def main():
    """Run complete pipeline"""
    print("\n" + "="*70)
    print("🏥 HEALTHCARE DATA PIPELINE")
    print("="*70)
    
    # Step 1: Extract
    print_progress("Extracting data...", 1, 3)
    raw_data = extract_all_data()
    
    # Check if we have any data
    has_data = False
    for key, value in raw_data.items():
        if value is not None and len(value) > 0:
            has_data = True
            break
    
    if not has_data:
        print("\n❌ No data found. Please place CSV files in C:\\FED-PROJECT\\Project dataset\\data\\")
        return
    
    # Step 2: Transform
    print_progress("Transforming data...", 2, 3)
    transformed_data, insights = transform_all_data(raw_data)
    
    if transformed_data is None or len(transformed_data) == 0:
        print("\n❌ Transformation failed")
        return
    
    # Step 3: Load
    print_progress("Loading to database...", 3, 3)
    success = load_to_database(transformed_data)
    
    print_progress("Pipeline complete!", 3, 3)
    print()
    
    if success:
        print("\n" + "="*70)
        print("✅ PIPELINE EXECUTED SUCCESSFULLY!")
        print("="*70)
        
        print("\n📊 SUMMARY STATISTICS:")
        if insights:
            print(f"   • Total Records: {insights.get('total_records', 0):,}")
            print(f"   • Total Patients: {insights.get('total_patients', 0):,}")
            print(f"   • Total Doctors: {insights.get('total_doctors', 0):,}")
            print(f"   • Total Revenue: ${insights.get('total_revenue', 0):,.2f}")
            print(f"   • Average Cost: ${insights.get('avg_cost', 0):,.2f}")
        
        if insights and insights.get('doctor_revenue'):
            print("\n🏆 TOP PERFORMERS:")
            for i, (doctor, revenue) in enumerate(list(insights.get('doctor_revenue', {}).items())[:5], 1):
                print(f"   {i}. {doctor}: ${revenue:,.2f}")
        
        print("\n🎯 NEXT STEPS:")
        print("   1. Launch dashboard: cd dashboard && streamlit run app.py")
        print("   2. Explore interactive visualizations")
        print("   3. Apply filters to analyze specific segments")

if __name__ == "__main__":
    main()