
import sqlite3
import pandas as pd
import os
from pathlib import Path

def get_db_path():
    """Get database file path"""
    return Path(__file__).parent.parent / 'database' / 'healthcare.db'

def create_connection():
    """Create database connection"""
    db_path = get_db_path()
    
    # Ensure database directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    return conn

def load_to_database(df, table_name='healthcare_data'):
    """Load dataframe to SQLite database"""
    print("\n" + "="*50)
    print("💾 LOADING TO DATABASE")
    print("="*50)
    
    try:
        conn = create_connection()
        
        # Save to database
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # Get record count
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Loaded {count} records to database")
        print(f"   Database location: {get_db_path()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading to database: {e}")
        return False

def query_database(query=None, table_name='healthcare_data'):
    """Query data from database"""
    try:
        conn = create_connection()
        
        if query is None:
            query = f"SELECT * FROM {table_name}"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
        
    except Exception as e:
        print(f"❌ Error querying database: {e}")
        return None

def get_table_info():
    """Get information about database tables"""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        info = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            info[table_name] = count
        
        conn.close()
        return info
        
    except Exception as e:
        print(f"❌ Error getting table info: {e}")
        return {}