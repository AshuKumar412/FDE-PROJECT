 
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(42)
np.random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ── Doctors ──────────────────────────────────────────────────────────────────
SPECIALIZATIONS = ["Cardiology","Neurology","Orthopedics","Pediatrics",
                   "Oncology","Dermatology","Gastroenterology","Psychiatry",
                   "Endocrinology","General Practice"]

doctors = pd.DataFrame({
    "doctor_id":      [f"D{i:03d}" for i in range(1, 11)],
    "doctor_name":    [f"Dr. {n}" for n in [
        "Arjun Mehta","Priya Sharma","Ravi Kumar","Sunita Patel",
        "Vikram Singh","Anjali Rao","Suresh Iyer","Kavitha Nair",
        "Rajesh Gupta","Deepa Reddy"]],
    "specialization": SPECIALIZATIONS,
    "experience_years": np.random.randint(5, 30, 10),
    "consultation_fee": np.random.randint(500, 3000, 10),
    "hospital":       np.random.choice(["Apollo","AIIMS","Fortis","Max","Medanta"], 10),
})

# ── Patients ─────────────────────────────────────────────────────────────────
FIRST = ["Aarav","Aditya","Ananya","Arjun","Bhavya","Chetan","Deepika",
         "Divya","Esha","Farhan","Gaurav","Harini","Ishaan","Jaya","Karan",
         "Kavya","Lakshmi","Manish","Meera","Mohan","Nandini","Nikhil",
         "Pallavi","Pradeep","Priyanka","Rahul","Riya","Rohit","Sachin",
         "Sandhya","Sanjay","Shruti","Siddharth","Sneha","Suresh",
         "Tanvi","Usha","Varun","Vidya","Vijay","Vinay","Vivek",
         "Yamini","Yash","Zara","Arun","Bharat","Chandra","Dhruv","Ekta"]
LAST  = ["Sharma","Patel","Singh","Kumar","Rao","Gupta","Nair","Reddy",
         "Iyer","Joshi","Mishra","Verma","Tiwari","Pandey","Desai",
         "Shah","Mehta","Pillai","Menon","Bose"]

patients = pd.DataFrame({
    "patient_id":   [f"P{i:03d}" for i in range(1, 51)],
    "patient_name": [f"{random.choice(FIRST)} {random.choice(LAST)}" for _ in range(50)],
    "date_of_birth":[
        (datetime(1990,1,1) - timedelta(days=random.randint(365*5, 365*75))).strftime("%Y-%m-%d")
        for _ in range(50)],
    "gender":       np.random.choice(["Male","Female","Other"], 50, p=[0.48,0.48,0.04]),
    "blood_group":  np.random.choice(["A+","A-","B+","B-","O+","O-","AB+","AB-"], 50),
    "city":         np.random.choice(["Hyderabad","Mumbai","Delhi","Bangalore",
                                       "Chennai","Kolkata","Pune","Ahmedabad"], 50),
    "phone":        [f"9{random.randint(100000000,999999999)}" for _ in range(50)],
    "insurance":    np.random.choice(["Yes","No"], 50, p=[0.6,0.4]),
})

# ── Appointments ─────────────────────────────────────────────────────────────
start = datetime(2024, 1, 1)
appointments = pd.DataFrame({
    "appointment_id": [f"A{i:04d}" for i in range(1, 201)],
    "patient_id":     np.random.choice(patients["patient_id"], 200),
    "doctor_id":      np.random.choice(doctors["doctor_id"],   200),
    "appointment_date":[
        (start + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")
        for _ in range(200)],
    "appointment_time": [f"{random.randint(8,17):02d}:{random.choice(['00','15','30','45'])}"
                         for _ in range(200)],
    "status":         np.random.choice(
        ["Completed","Scheduled","Cancelled","No-Show"], 200, p=[0.65,0.2,0.1,0.05]),
    "visit_type":     np.random.choice(
        ["New Patient","Follow-up","Emergency","Routine Checkup"], 200, p=[0.25,0.45,0.1,0.2]),
})

# ── Billing ───────────────────────────────────────────────────────────────────
billing = pd.DataFrame({
    "billing_id":     [f"B{i:04d}" for i in range(1, 201)],
    "patient_id":     appointments["patient_id"].values,
    "appointment_id": appointments["appointment_id"].values,
    "amount":         np.round(np.random.uniform(500, 5000, 200), 2),
    "payment_method": np.random.choice(
        ["Cash","Credit Card","UPI","Insurance","Net Banking"], 200, p=[0.2,0.25,0.3,0.15,0.1]),
    "payment_status": np.random.choice(["Paid","Pending","Partial"], 200, p=[0.75,0.15,0.10]),
    "billing_date":   appointments["appointment_date"].values,
})

# ── Treatments ────────────────────────────────────────────────────────────────
TREATMENTS = ["Consultation","Blood Test","X-Ray","MRI Scan","CT Scan",
              "ECG","Ultrasound","Surgery","Physiotherapy","Vaccination",
              "Chemotherapy","Dialysis","Endoscopy","Biopsy","Eye Test"]
treatments = pd.DataFrame({
    "treatment_id":   [f"T{i:04d}" for i in range(1, 201)],
    "appointment_id": np.random.choice(appointments["appointment_id"], 200),
    "treatment_name": np.random.choice(TREATMENTS, 200),
    "duration_mins":  np.random.choice([15,30,45,60,90,120], 200),
    "outcome":        np.random.choice(["Successful","Ongoing","Referred","Inconclusive"], 200,
                                        p=[0.65,0.2,0.1,0.05]),
    "notes":          ["Standard procedure" for _ in range(200)],
})

# ── Save ──────────────────────────────────────────────────────────────────────
doctors.to_csv(    f"{DATA_DIR}/doctors.csv",      index=False)
patients.to_csv(   f"{DATA_DIR}/patients.csv",     index=False)
appointments.to_csv(f"{DATA_DIR}/appointments.csv",index=False)
billing.to_csv(    f"{DATA_DIR}/billing.csv",      index=False)
treatments.to_csv( f"{DATA_DIR}/treatments.csv",   index=False)

print("✅ Sample data generated successfully!")
for name, df in [("doctors",doctors),("patients",patients),
                  ("appointments",appointments),("billing",billing),("treatments",treatments)]:
    print(f"   {name:15s}: {len(df):>4d} rows")