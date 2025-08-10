import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def load_csv_to_database():
    """Load CSV data into PostgreSQL database hosted on Render"""
    
    # Get database URL from environment
    database_url = os.getenv('SQLALCHEMY_DATABASE_URI')
    
    if not database_url:
        print("Error: SQLALCHEMY_DATABASE_URI not found in environment variables")
        return
    
    try:
        # Create SQLAlchemy engine
        engine = create_engine(database_url)
        
        # Read CSV file
        print("Reading CSV file...")
        df = pd.read_csv('bank.csv')
        print(f"Loaded {len(df)} rows from CSV")
        
        # Load data in chunks to avoid memory issues
        chunk_size = 1000
        
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()
            
            try:
                print("Loading data into database...")
                
                # Load data in chunks
                for i in range(0, len(df), chunk_size):
                    chunk = df.iloc[i:i+chunk_size]
                    
                    # Insert chunk using to_sql
                    chunk.to_sql(
                        'branches', 
                        conn, 
                        if_exists='append',
                        index=False,
                        method='multi'
                    )
                    
                    print(f"Loaded {min(i+chunk_size, len(df))}/{len(df)} rows")
                
                # Commit transaction
                trans.commit()
                print("Data loaded successfully!")
                
            except Exception as e:
                # Rollback on error
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
            # Get unique bank_ids and create banks table
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
    
    # First load the branches data
    load_csv_to_database()
    
    # Then create banks table entries
    create_banks_table()
    
    print("Data load process completed!")
