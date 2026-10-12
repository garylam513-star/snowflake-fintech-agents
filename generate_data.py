import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_credit_card_data(num_rows=500, filename="data/mock_credit_card_transactions.csv"):
    card_types = ["Visa", "Mastercard", "AMEX", "Discover"]
    currencies = ["USD", "EUR", "GBP", "CAD"]
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "TRANSACTION_ID", "TIMESTAMP", "CARD_NUMBER", "CARD_TYPE", 
            "HOLDER_NAME", "MERCHANT_NAME", "MERCHANT_CATEGORY", 
            "AMOUNT", "CURRENCY", "IS_FRAUD"
        ])
        
        start_time = datetime.now() - timedelta(hours=24)
        for i in range(num_rows):
            tx_id = 1000000000 + i
            tx_time = start_time + timedelta(seconds=i * random.randint(10, 60))
            
            is_fraud = 1 if random.random() < 0.03 else 0
            if is_fraud:
                amount = round(random.uniform(1500.00, 5000.00), 2)
            else:
                amount = round(random.uniform(5.50, 150.00), 2)
                
            writer.writerow([
                tx_id, 
                tx_time.strftime("%Y-%m-%d %H:%M:%S"), 
                fake.credit_card_number(),
                random.choice(card_types), 
                fake.name(), 
                fake.company() + " " + random.choice(["Store", "Inc", "LLC"]),
                random.choice(["Retail", "Groceries", "Entertainment", "Travel", "Gas"]),
                amount, 
                random.choice(currencies), 
                is_fraud
            ])
            
    print(f"📊 Success! Generated {num_rows} transactions in '{filename}'.")

if __name__ == "__main__":
    # Explicitly targeted 500 rows limit
    generate_credit_card_data(num_rows=500)
