import pandas as pd
import logging

brand_category_mapping={
    'Tesco': 'Groceries',
    'Sainsbury\'s': 'Groceries',
    'Lidl': 'Groceries',
    'Asda': 'Groceries',
    'M&S Foods': 'Groceries',
    'Waitrose': 'Groceries',
    'Amazon': 'Shopping',
    'ebay': 'Shopping',
    'shein': 'Shopping',
    'Temu': 'Shopping',
    'Walmart': 'Shopping',
    'Iceland': 'Shopping',
    'Uber': 'Transport',
    'Starbucks': 'Food & Drink',
    'Nandos': 'Food & Drink',
    'Preat A Manger': 'Food & Drink',
    'Costa': 'Food & Drink',
    'Gails': 'Food & Drink',
    'Cafe': 'Food & Drink',
    'Coffee': 'Food & Drink',
    'Greggs': 'Food & Drink',
    'Restaurent': 'Food & Drink',
    'Wagamama': 'Food & Drink',
    'McDonalds': 'Food & Drink',
    'TFL': 'Transport',
    'Cineworld': 'Entertainment',
    'Odeon': 'Entertainment',
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

logging.basicConfig(level=logging.INFO)

def process_data(data):
    # Define the column name mappings for dynamic columns
    column_mapping = {
        'amount': 'Amount',
        'cost': 'Amount',
        'price': 'Amount',
    }

     # Rename columns based on the mapping
    old_columns = list(data.columns)
    data.columns = [column_mapping.get(col.lower(), col) for col in data.columns]
    
    # Log which columns were renamed
    renamed_columns = {old: new for old, new in zip(old_columns, data.columns) if old != new}
    if renamed_columns:
        logging.info(f"Renamed columns: {renamed_columns}")

    # Check if required columns are present
    if 'Amount' not in data.columns or 'Merchant' not in data.columns:
        raise ValueError("Required columns 'Amount' and 'Merchant' are missing from the file.")

    # Remove irrelevant columns (like 'TransactionID', 'Timestamp', etc.)
    irrelevant_columns = ['TransactionID', 'Timestamp', 'UserID', 'PaymentMethod']
    data = data.drop(columns=[col for col in irrelevant_columns if col in data.columns])

    # Convert 'Amount' to numeric
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

    # Apply categorization logic based on merchant (brand)
    data['Category'] = data['Merchant'].apply(lambda x: brand_category_mapping.get(x, 'Other'))

    # Summarize the data by category and brand
    brand_category_summary = data.groupby(['Merchant', 'Category'])['Amount'].sum().reset_index()

    # Get overall spending by brand
    overall_spending = data.groupby('Merchant')['Amount'].sum().reset_index()

    return brand_category_summary, overall_spending