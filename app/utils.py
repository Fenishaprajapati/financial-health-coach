import joblib
import pandas as pd

# Load the trained model
model = joblib.load('models/merchant_classifier.pkl')

# Possible column name mappings for 'Amount' and 'Merchant'
column_name_mapping = {
    'Amount': ['amount', 'price', 'total_amount', 'cost'],
    'Merchant': ['merchant', 'seller', 'brand', 'company', 'store']
}

# Function to predict the category for a new merchant
def predict_category(merchant):
    return model.predict([merchant])[0]

# Function to standardize columns in the uploaded CSV file
def standardize_columns(data):
    # Standardize 'Amount' column name
    for standard_col, variations in column_name_mapping.items():
        for var in variations:
            if var in data.columns.str.lower():
                data = data.rename(columns={var: standard_col})
                break
    
    # Ensure 'Merchant' and 'Amount' columns are present
    if 'Merchant' not in data.columns or 'Amount' not in data.columns:
        raise ValueError("Required columns 'Merchant' and 'Amount' are missing or misnamed in the file.")
    
    return data

def check_budget_spending(processed_data, budget_goals):
    alerts = []

    # Compare actual spending with budget goals
    for index, row in processed_data.iterrows():
        category = row['Category']
        amount_spent = row['Amount']

        if category in budget_goals:
            budget = budget_goals[category]
            if amount_spent > budget:
                alert = f"Alert: You have overspent on {category} by £{amount_spent - budget:.2f}."
                alerts.append(alert)
            else:
                alert = f"Good job! You are within the budget for {category}."
                alerts.append(alert)

    # If no alerts, return a positive summary
    if not alerts:
        alerts.append("Great! You are within your overall budget for all categories.")

    return alerts
