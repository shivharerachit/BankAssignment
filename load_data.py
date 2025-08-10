import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def load_csv_to_database():
    """Load CSV data into PostgreSQL database hosted on Render"""
    database_url = os.getenv('SQLALCHEMY_DATABASE_URI')
    
    if not database_url:
        print("Error: SQLALCHEMY_DATABASE_URI not found in environment variables")
        return
    
    try:
        engine = create_engine(database_url)
        
        print("Reading CSV file...")
        df = pd.read_csv('bank.csv')
        print(f"Loaded {len(df)} rows from CSV")
        
        chunk_size = 1000
        
        with engine.connect() as conn:
            trans = conn.begin()
            
            try:
                print("Loading data into database...")
                for i in range(0, len(df), chunk_size):
                    chunk = df.iloc[i:i+chunk_size]
                    chunk.to_sql(
                        'branches', 
                        conn, 
                        if_exists='append',
                        index=False,
                        method='multi'
                    )
                    print(f"Loaded {min(i+chunk_size, len(df))}/{len(df)} rows")

                trans.commit()
                print("Data loaded successfully!")
                
            except Exception as e:
                trans.rollback()
                print(f"Error loading data: {e}")
                raise
                
    except Exception as e:
        print(f"Database connection error: {e}")

def create_banks_table():
    """Create and populate banks table from unique bank_ids"""
    
    database_url = os.getenv('SQLALCHEMY_DATABASE_URI')
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO banks (id, name)
                SELECT DISTINCT 
                    bank_id,
                    CASE 
                        WHEN bank_id = 60 THEN 'ABHYUDAYA COOPERATIVE BANK LIMITED'
                        -- Add more bank mappings as needed
                        ELSE 'Unknown Bank ' || bank_id
                    END as name
                FROM branches
                WHERE NOT EXISTS (SELECT 1 FROM banks WHERE id = bank_id)
            """)
            
            result = conn.execute(query)
            conn.commit()
            print(f"Created {result.rowcount} bank records")
            
    except Exception as e:
        print(f"Error creating banks: {e}")

if __name__ == "__main__":
    print("Starting data load process...")
    load_csv_to_database()
    create_banks_table()
    print("Data load process completed!")
