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
    filename=LOG_FILENAME, level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', force=True 
)

KEY_FILENAME = "encryption.key"
PII_COLUMNS = ['full_name', 'account_number']

def get_or_create_key():
    if os.path.exists(KEY_FILENAME):
        with open(KEY_FILENAME, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILENAME, "wb") as key_file:
            key_file.write(key)
        return key

def encrypt_data(data_string, cipher_suite):
    return cipher_suite.encrypt(str(data_string).encode('utf-8')).decode('utf-8')

def process_data():
    logging.info("--- Data Processing Job Started ---")
    if not os.path.exists(FILENAME):
        logging.error(f"Input file {FILENAME} missing.")
        return

    start_time = time.perf_counter()
    df = pd.read_csv(FILENAME)
    cipher_suite = Fernet(get_or_create_key())
    
    encrypt_start = time.perf_counter()
    for col in PII_COLUMNS:
        if col in df.columns:
            df[col + '_encrypted'] = df[col].apply(lambda x: encrypt_data(x, cipher_suite))
            df = df.drop(columns=[col])
            logging.info(f"Encrypted column: {col}")
    
    encrypt_end = time.perf_counter()
    logging.info(f"Encryption completed in {encrypt_end - encrypt_start:.4f}s")
    
    df.to_csv(SECURED_FILENAME, index=False)
    
    total_time = time.perf_counter() - start_time
    logging.info(f"KPI - Total Processing Time: {total_time:.4f} seconds")
    logging.info("--- Data Processing Job Finished ---")

if __name__ == "__main__":
    process_data()