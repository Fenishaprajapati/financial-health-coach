import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta

# Merchant-category mapping
merchant_category_dict = {
    'Tesco': 'Groceries',
    'Sainsbury\'s': 'Groceries',
    'Asda': 'Groceries',
    'Waitrose': 'Groceries',
    'Iceland': 'Groceries',
    'Starbucks': 'Food & Drink',
    'McDonalds': 'Food & Drink',
    'Amazon': 'Shopping',
    'Uber': 'Transport',
    'Netflix': 'Entertainment',
    'Argos': 'Shopping',
    'Greggs': 'Food & Drink',
    'Nandos': 'Food & Drink',
    'Wagamama': 'Food & Drink',
    'Cineworld': 'Entertainment',
    'O2': 'Mobile Services',
    'EE': 'Mobile Services',
    'Vodafone': 'Mobile Services',
    'Three': 'Mobile Services'
}

# Predefined alternative merchants for overspent categories
alternative_merchants = {
    'Groceries': ['Aldi', 'Lidl', 'Waitrose'],
    'Food & Drink': ['Costa', 'Greggs', 'Pret A Manger'],
    'Transport': ['TFL', 'Uber', 'National Rail'],
    'Entertainment': ['Cineworld', 'Odeon', 'Vue'],
    'Shopping': ['Primark', 'eBay', 'Charity Shops'],
    'Mobile Services': ['Giffgaff', 'Three', 'Virgin Mobile']
}

# Generate synthetic data for a single user
def generate_synthetic_data(num_rows=1000):
    data = {
        'Merchant': [random.choice(list(merchant_category_dict.keys())) for _ in range(num_rows)],  # Random merchant
        'Amount': [round(random.uniform(5, 500), 2) for _ in range(num_rows)],  # Random spending amounts
        'Date': [random_date(datetime(2023, 1, 1), datetime(2023, 12, 31)) for _ in range(num_rows)],
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Add the Category column based on Merchant using the merchant-category dictionary
    df['Category'] = df['Merchant'].map(merchant_category_dict)

    # Add the Spending History column (for single user, list all merchants)
    df['Spending History'] = ', '.join(df['Merchant'])

    # Add 'Overspend' column based on budget comparison
    user_budget_goals = {
        "Groceries": 500,
        "Transport": 100,
        "Food & Drink": 200,
        "Entertainment": 150,
        "Shopping": 300,
        "Utilities & Bills": 250,
        "Mobile Services": 100
    }
    df['Overspend'] = df.apply(lambda row: 'Overspent' if row['Amount'] > user_budget_goals.get(row['Category'], 0) else 'Within Budget', axis=1)

    # Add 'Alternative Recommendation' column based on overspend
    def recommend_alternatives(row):
        if row['Overspend'] == 'Overspent':
            category = row['Category']
            used_merchants = row['Spending History']
            alternatives = [merchant for merchant in alternative_merchants.get(category, []) if merchant not in used_merchants]
            return alternatives[0] if alternatives else 'No alternative'
        return 'N/A'

    df['Alternative Recommendation'] = df.apply(recommend_alternatives, axis=1)

    return df

# Function to generate random dates
def random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Generate the synthetic dataset
synthetic_data = generate_synthetic_data(num_rows=1000)

# Save to CSV
synthetic_data.to_csv('data/synthetic_transactions_1000.csv', index=False)

#just show the synthetic data
print(synthetic_data.head())
