import pandas as pd
import numpy as np

np.random.seed(42)

# More merchants per category clearly provided
merchant_categories = {
    'Shopping': ['Amazon', 'Argos', 'John Lewis', 'Primark', 'ASOS', 'eBay', 'Zara'],
    'Food & Drink': ['Starbucks', 'Costa', 'Pret A Manger', 'Greggs', 'McDonald\'s', 'Burger King', 'Nando\'s', 'KFC'],
    'Groceries': ['Tesco', 'Sainsbury\'s', 'Waitrose', 'Aldi', 'Lidl', 'Iceland', 'Morrisons'],
    'Transport': ['Uber', 'Bolt', 'TFL', 'National Rail'],
    'Entertainment': ['Netflix', 'Disney+', 'Vue', 'Spotify', 'Apple Music'],
    'Utilities & Bills': ['EDF', 'Octopus Energy', 'British Gas', 'Thames Water'],
    'Mobile Services': ['Giffgaff', 'Virgin Mobile', 'Sky Mobile', 'Vodafone']
}

# Generate synthetic transactions
records = []
for _ in range(5000):  # Larger dataset for improved training clearly
    category = np.random.choice(list(merchant_categories.keys()))
    merchant = np.random.choice(merchant_categories[category])
    amount = np.round(np.random.uniform(5, 250), 2)
    user = np.random.randint(1, 201)  # More users clearly
    records.append({'Merchant': merchant, 'Category': category, 'Amount': amount, 'User': user})

df_rich = pd.DataFrame(records)
df_rich.to_csv('data/rich_synthetic_transactions.csv', index=False)
