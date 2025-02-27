import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Corrected training data with equal length for each list
train_data = {
    'Merchant': [
        'Tesco', 'Sainsburys', 'Asda', 'Morrisons', 'Aldi', 'Lidl', 'Waitrose', 'Iceland', 
        'Starbucks', 'Uber', 'Amazon', 'Walmart', 'Amazon UK', 'Argos', 'John Lewis', 
        'McDonalds', 'Greggs', 'Pret A Manger', 'Nandos', 'Wagamama', 'Cineworld', 
        'Odeon', 'Netflix UK', 'Spotify', 'British Gas', 'O2', 'Vodafone', 'EE', 'Thames Water'
    ],
    'Category': [
        'Groceries', 'Groceries', 'Groceries', 'Groceries', 'Groceries', 'Groceries', 'Groceries', 'Groceries',
        'Food & Drink', 'Transport', 'Shopping', 'Groceries', 'Shopping', 'Shopping', 'Shopping',
        'Food & Drink', 'Food & Drink', 'Food & Drink', 'Food & Drink', 'Food & Drink', 'Entertainment',
        'Entertainment', 'Entertainment', 'Utilities & Bills', 'Mobile Services', 'Mobile Services', 'Mobile Services', 'Utilities & Bills', 'Transport'
    ]
}

# Ensure the lengths of 'Merchant' and 'Category' lists are the same
assert len(train_data['Merchant']) == len(train_data['Category']), "Lists have different lengths!"

# Convert the training data to a DataFrame
df_train = pd.DataFrame(train_data)

# Create a machine learning pipeline with TfidfVectorizer and MultinomialNB
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(df_train['Merchant'], df_train['Category'])

# Function to predict the category of a new transaction based on the merchant
def predict_category(merchant):
    return model.predict([merchant])[0]

# Function to process the transaction data
def process_data(data):
    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Extract year and month from the 'Date' column for monthly aggregation
    data['YearMonth'] = data['Date'].dt.to_period('M')

    # Convert the 'Amount' column to numeric
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

    # Apply the trained ML model to categorize the transactions
    data['Category'] = data['Merchant'].apply(predict_category)

    # Group by 'YearMonth' and 'Category' and sum the 'Amount' to get monthly spending per category
    monthly_summary = data.groupby(['YearMonth', 'Category'])['Amount'].sum().reset_index()

    return monthly_summary
