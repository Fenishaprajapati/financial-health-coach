import pandas as pd
import random
import string
from datetime import datetime, timedelta

# Define Merchant-Category Mapping
merchant_category_mapping = {
    'Tesco': 'Groceries',
    'Sainsbury\'s': 'Groceries',
    'Waitrose': 'Groceries',
    'ASDA': 'Groceries',
    'John Lewis': 'Retail',
    'Boots': 'Retail',
    'B&Q': 'Home & Garden',
    'Iceland': 'Groceries',
    'Greggs': 'Food & Drink',
    'Starbucks': 'Food & Drink',
    'Cineworld': 'Entertainment',
    'Odeon': 'Entertainment',
    'Uber': 'Transport',
    'Amazon UK': 'Shopping',
    'Currys PC World': 'Electronics',
    'IKEA': 'Home & Garden',
    'Argos': 'Retail',
    'Zara': 'Clothing',
    'H&M': 'Clothing', 
    'Lidl': 'Groceries',
    'M&S Foods': 'Groceries',
    'Amazon': 'Shopping',
    'ebay': 'Shopping',
    'shein': 'Shopping',
    'Temu': 'Shopping',
    'Walmart': 'Shopping',
    'Iceland': 'Shopping',
    'John Lewis': 'Shopping',
    'Uber': 'Transport',
    'Starbucks': 'Food & Drink',
    'Nandos': 'Food & Drink',
    'Pret A Manger': 'Food & Drink',
    'Costa': 'Food & Drink',
    'Gails': 'Food & Drink',
    'Cafe': 'Food & Drink',
    'Coffee': 'Food & Drink',
    'Greggs': 'Food & Drink',
    'Restaurent': 'Food & Drink',
    'Wagamama': 'Food & Drink',
    'McDonald\'s': 'Food & Drink',
    'TFL': 'Transport',
    'Netflix UK': 'Entertainment',
    'Spotify': 'Entertainment',
    'Cineworld': 'Entertainment',
    'O2': 'Mobile Services',
    'EE': 'Mobile Services',
    'Vodafone': 'Mobile Services',
    'Three': 'Mobile Services',
    'Thames Water': 'Utilities & Bills',
    'British Gas': 'Utilities & Bills',
}

# Define payment methods
payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Cash', 'Mobile']

# Generate synthetic data
num_rows = 300  # Creating 300 rows of data
amounts = [random.uniform(5, 500) for _ in range(num_rows)]  # Random amounts between 5 and 500
merchants_list = [random.choice(list(merchant_category_mapping.keys())) for _ in range(num_rows)]
categories_list = [merchant_category_mapping[merchant] for merchant in merchants_list]  # Assign correct category based on merchant
payment_methods_list = [random.choice(payment_methods) for _ in range(num_rows)]
transaction_ids = [''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) for _ in range(num_rows)]

# Generate random timestamps within the last 30 days
timestamp_start = datetime(2025, 2, 1, 10, 0, 0)
timestamps = [(timestamp_start + timedelta(minutes=random.randint(1, 1440))).strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_rows)]

# Create the DataFrame
data = {
    'Merchant': merchants_list,
    'Amount': amounts,
    'TransactionID': transaction_ids,
    'PaymentMethod': payment_methods_list,
    'Category': categories_list,
    'Timestamp': timestamps
}

df = pd.DataFrame(data)

# Save to CSV
df.to_csv('data/synthetic_transactions_300.csv', index=False)
print("Synthetic data created and saved as 'synthetic_transactions_300.csv'")
