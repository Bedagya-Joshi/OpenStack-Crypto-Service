import csv
import random
import string
import os

TARGET_SIZE_MB = 5  
FILENAME = "small_dataset.csv"

FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
NOTE_TEMPLATES = [
    "Monthly rent payment", 
    "Salary direct deposit", 
    "Utility bill transfer", 
    "Grocery store purchase", 
    "Investment fund deposit", 
    "Online shopping transaction"
]

def create_small_csv():
    print(f"Generating {TARGET_SIZE_MB}MB realistic dataset...")
    
    with open(FILENAME, 'w', newline='') as csvfile:
        fieldnames = ['id', 'full_name', 'account_number', 'credit_card', 'balance', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        row_id = 1
        while os.path.getsize(FILENAME) < (TARGET_SIZE_MB * 1024 * 1024):
            writer.writerow({
                'id': row_id,
                'full_name': f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                'account_number': ''.join(random.choices(string.digits, k=10)),
                'credit_card': f"{random.randint(4000, 4999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                'balance': round(random.uniform(100.0, 50000.0), 2),
                'notes': random.choice(NOTE_TEMPLATES)
            })
            row_id += 1
            
    print(f"Done! Created '{FILENAME}'")

if __name__ == "__main__":
    create_small_csv()