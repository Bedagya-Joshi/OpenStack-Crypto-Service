import pandas as pd
from cryptography.fernet import Fernet
import time
import os
import logging
from dotenv import load_dotenv

load_dotenv()
FILENAME = os.getenv("DATA_FILE", "large_dataset.csv")
base_name = os.path.splitext(FILENAME)[0]
SECURED_FILENAME = f"secured_{base_name}.csv"
LOG_FILENAME = f"{base_name}_processor.log"

logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True 
)

KEY_FILENAME = "encryption.key"

def generate_encryption_key():
    key = Fernet.generate_key()
    with open(KEY_FILENAME, "wb") as key_file:
        key_file.write(key)
    return key

def encrypt_data(data_string, cipher_suite):
    encoded_text = str(data_string).encode('utf-8')
    return cipher_suite.encrypt(encoded_text).decode('utf-8')

def process_data():
    logging.info("--- Data Processing Job Started ---")
    
    if not os.path.exists(FILENAME):
        logging.error(f"Input file {FILENAME} missing.")
        return

    start_time = time.perf_counter() 
    
    df = pd.read_csv(FILENAME)
    load_time = time.perf_counter()
    logging.info(f"Loaded {len(df):,} records in {load_time - start_time:.4f}s")
    
    cipher_suite = Fernet(generate_encryption_key())
    
    encrypt_start = time.perf_counter()
    df['credit_card_encrypted'] = df['credit_card'].apply(lambda x: encrypt_data(x, cipher_suite))
    df = df.drop(columns=['credit_card'])
    encrypt_end = time.perf_counter()
    logging.info(f"Encryption completed in {encrypt_end - encrypt_start:.4f}s")
    
    total_balance = df['balance'].sum()
    
    df.to_csv(SECURED_FILENAME, index=False)
    
    total_time = time.perf_counter() - start_time
    logging.info(f"KPI - Total Portfolio Balance: ${total_balance:,.2f}")
    logging.info(f"KPI - Total Processing Time: {total_time:.4f} seconds")
    logging.info("--- Data Processing Job Finished ---")

if __name__ == "__main__":
    process_data()