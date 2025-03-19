# import joblib
# import pandas as pd

# # Load clearly trained models (no label encoder needed here)
# category_model = joblib.load('models/merchant_classifier.pkl')
# recommendation_model = joblib.load('models/merchant_recommendations_classifier.pkl')

# # Standardize CSV columns
# def standardize_columns(data):
#     column_name_mapping = {
#         'Amount': ['amount', 'price', 'total_amount', 'cost'],
#         'Merchant': ['merchant', 'seller', 'brand', 'company', 'name']
#     }
#     for standard_col, variations in column_name_mapping.items():
#         for var in variations:
#             if var in data.columns.str.lower():
#                 data.rename(columns={var: standard_col}, inplace=True)
#                 break

#     if 'Merchant' not in data.columns or 'Amount' not in data.columns:
#         raise ValueError("Columns 'Merchant' and 'Amount' must be present.")

#     return data

# # Predict spending category of merchant
# def predict_category(merchant):
#     return category_model.predict([merchant])[0]

# # Check overall budget and alert for overspending
# def check_budget_alerts(data, budget_goals):
#     alerts = []
#     overspent_categories = []

#     category_spending = data.groupby('Category')['Amount'].sum()

#     for category, budget in budget_goals.items():
#         spent = category_spending.get(category, 0)
#         if spent > budget:
#             overspent_amount = spent - budget
#             alerts.append(f"Alert: Overspent on {category} by £{overspent_amount:.2f}.")
#             overspent_categories.append(category)
#         else:
#             alerts.append(f"Good job! You are within the budget for {category}.")

#     return alerts, overspent_categories

# # Directly predict alternative merchant (No encoding/decoding)
# def recommend_alternative_merchant(merchant):
#     alternative_merchant = recommendation_model.predict([merchant])[0]
#     return alternative_merchant
import joblib
import pandas as pd
import numpy as np

# Load your clearly trained models
merchant_recommendation_model = joblib.load('models/merchant_to_merchant_model.pkl')
category_model = joblib.load('models/merchant_to_category_model.pkl')
similarity_matrix = joblib.load('models/merchant_similarity_matrix.pkl')
vectorizer = joblib.load('models/merchant_tfidf_vectorizer.pkl')
unique_merchants = joblib.load('models/unique_merchants.pkl')

# Predict category
def predict_category(merchant):
    return category_model.predict([merchant])[0]

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

# Budget check
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

def recommend_alternative_merchant(merchant):
    predicted_category = category_model.predict([merchant])[0]

    if merchant not in unique_merchants:
        return "No alternative available"

    merchant_idx = np.where(unique_merchants == merchant)[0][0]
    merchant_similarities = similarity_matrix[merchant_idx].copy()
    merchant_similarities[merchant_idx] = -1
    similar_merchants_idx = np.argsort(merchant_similarities)[::-1]

    for idx in similar_merchants_idx:
        candidate_merchant = unique_merchants[idx]
        candidate_category = category_model.predict([candidate_merchant])[0]
        if candidate_category == predicted_category:
            return candidate_merchant

    merchants_df = pd.DataFrame({
        'Merchant': unique_merchants,
        'Category': category_model.predict(unique_merchants)
    })

    alternatives_in_category = merchants_df[
        (merchants_df['Category'] == predicted_category) &
        (merchants_df['Merchant'] != merchant)
    ]

    if not alternatives_in_category.empty:
        return alternatives_in_category.sample(1).iloc[0]['Merchant']

    return "No alternative available"