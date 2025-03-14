import joblib
import pandas as pd

# Load clearly trained models (no label encoder needed here)
category_model = joblib.load('models/merchant_classifier.pkl')
recommendation_model = joblib.load('models/merchant_recommendations_classifier.pkl')

# Standardize CSV columns
def standardize_columns(data):
    column_name_mapping = {
        'Amount': ['amount', 'price', 'total_amount', 'cost'],
        'Merchant': ['merchant', 'seller', 'brand', 'company', 'name']
    }
    for standard_col, variations in column_name_mapping.items():
        for var in variations:
            if var in data.columns.str.lower():
                data.rename(columns={var: standard_col}, inplace=True)
                break

    if 'Merchant' not in data.columns or 'Amount' not in data.columns:
        raise ValueError("Columns 'Merchant' and 'Amount' must be present.")

    return data

# Predict spending category of merchant
def predict_category(merchant):
    return category_model.predict([merchant])[0]

# Check overall budget and alert for overspending
def check_budget_alerts(data, budget_goals):
    alerts = []
    overspent_categories = []

    category_spending = data.groupby('Category')['Amount'].sum()

    for category, budget in budget_goals.items():
        spent = category_spending.get(category, 0)
        if spent > budget:
            overspent_amount = spent - budget
            alerts.append(f"Alert: Overspent on {category} by £{overspent_amount:.2f}.")
            overspent_categories.append(category)
        else:
            alerts.append(f"Good job! You are within the budget for {category}.")

    return alerts, overspent_categories

# Directly predict alternative merchant (No encoding/decoding)
def recommend_alternative_merchant(merchant):
    alternative_merchant = recommendation_model.predict([merchant])[0]
    return alternative_merchant
