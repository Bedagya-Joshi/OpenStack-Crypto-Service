import csv
import random
import string
import os

FILENAME = "large_dataset.csv"
TARGET_SIZE_MB = 100  

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

def create_dummy_csv():
    print(f"Generating {TARGET_SIZE_MB}MB dataset... please wait.")
    
    with open(FILENAME, 'w', newline='') as csvfile:
        fieldnames = ['id', 'full_name', 'account_number', 'credit_card', 'balance', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        row_id = 1
        while os.path.getsize(FILENAME) < (TARGET_SIZE_MB * 1024 * 1024):
            writer.writerow({
                'id': row_id,
                'full_name': generate_random_string(15),
                'account_number': ''.join(random.choices(string.digits, k=10)),
                'credit_card': f"{random.randint(4000, 4999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                'balance': round(random.uniform(100.0, 50000.0), 2),
                'notes': generate_random_string(50) 
            })
            row_id += 1
            
            if row_id % 10000 == 0:
                current_size = os.path.getsize(FILENAME) / (1024 * 1024)
                print(f"Rows: {row_id}, Size: {current_size:.2f} MB")

    print(f"Done! Created '{FILENAME}' with size: {os.path.getsize(FILENAME) / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    create_dummy_csv()