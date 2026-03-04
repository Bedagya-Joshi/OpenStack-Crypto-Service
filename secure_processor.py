import pandas as pd
from cryptography.fernet import Fernet
import time
import os

FILENAME = "large_dataset.csv"
SECURED_FILENAME = "secured_dataset.csv"
KEY_FILENAME = "encryption.key"

def generate_encryption_key():
    """Generates and saves a secure key for Fernet encryption."""
    key = Fernet.generate_key()
    with open(KEY_FILENAME, "wb") as key_file:
        key_file.write(key)
    print(f"New encryption key generated and saved to {KEY_FILENAME}")
    return key

def encrypt_data(data_string, cipher_suite):
    """Encrypts a string using the provided Fernet cipher suite."""
    # Fernet requires bytes, so we encode the string, encrypt it, and decode the result back to a string
    encoded_text = str(data_string).encode('utf-8')
    encrypted_text = cipher_suite.encrypt(encoded_text)
    return encrypted_text.decode('utf-8')

def process_data():
    if not os.path.exists(FILENAME):
        print(f"Error: {FILENAME} not found. Please run generate_data.py first.")
        return

    print(f"Loading {FILENAME} into memory...")
    start_time = time.time()
    
    # 1. Load the data using Pandas
    df = pd.read_csv(FILENAME)
    print(f"Dataset successfully loaded. Total records: {len(df):,}")
    
    # 2. Setup Cryptography
    print("Initializing Fernet symmetric encryption...")
    encryption_key = generate_encryption_key()
    cipher_suite = Fernet(encryption_key)
    
    # 3. Secure the PII (Credit Card Numbers)
    print("Encrypting credit card numbers...")
    # Apply the encryption function to the entire credit_card column
    df['credit_card_encrypted'] = df['credit_card'].apply(lambda x: encrypt_data(x, cipher_suite))
    
    # Drop the original plain-text credit card column from the dataframe
    df = df.drop(columns=['credit_card'])
    
    # 4. Calculate a basic Business Analytics Metric (KPI)
    total_balance = df['balance'].sum()
    
    # 5. Save the secured dataset
    print(f"Saving encrypted data to {SECURED_FILENAME}...")
    df.to_csv(SECURED_FILENAME, index=False)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # 6. Output the final metrics
    print("\n" + "="*50)
    print("      SECURE DATA PROCESSING COMPLETE")
    print("="*50)
    print(f"Total Portfolio Balance : ${total_balance:,.2f}")
    print(f"Total Processing Time   : {processing_time:.2f} seconds")
    print("="*50)

if __name__ == "__main__":
    process_data()