import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load synthetic data
df = pd.read_csv('data/synthetic_transactions_1000.csv')

# Compute average spending per merchant and category
avg_spending = df.groupby(['Merchant', 'Category'])['Amount'].mean().reset_index()

# Function clearly defined to find cheaper alternative merchant dynamically
def find_cheaper_alternative(merchant, category, avg_spend_df):
    merchant_avg_amount = avg_spending.loc[avg_spending['Merchant'] == merchant, 'Amount'].values[0]

    cheaper_merchants = avg_spend_df[
        (avg_spend_df['Category'] == category) &
        (avg_spend_df['Amount'] < merchant_avg_amount) &
        (avg_spend_df['Merchant'] != merchant)
    ]

    if not cheaper_merchants.empty:
        return cheaper_merchants.sort_values('Amount').iloc[0]['Merchant']
    else:
        # if no cheaper merchant, randomly pick another merchant in the same category
        alternatives = avg_spending[
            (avg_spending['Category'] == category) &
            (avg_spending['Merchant'] != merchant)
        ]
        if not alternatives.empty:
            return alternatives.sample(1)['Merchant'].values[0]
        else:
            return merchant  # no alternative found

# Generate alternative merchant recommendations dynamically
avg_spending['RecommendedMerchant'] = avg_spending.apply(
    lambda row: find_cheaper_alternative(row['Merchant'], row['Category'], avg_spending), axis=1
)

# Merge with original data to assign recommendations
df = df.merge(avg_spending[['Merchant', 'RecommendedMerchant']], on='Merchant', how='left')

# Drop rows where merchant == recommended merchant (no good alternative found)
df = df[df['Merchant'] != df['RecommendedMerchant']]

# Train clearly defined Merchant-to-Merchant recommendation model (NO LabelEncoder)
X = df['Merchant']
y = df['RecommendedMerchant']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Clear pipeline (direct merchant names)
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(X_train, y_train)

# Evaluate clearly
accuracy = model.score(X_test, y_test)
print(f'Recommendation Model Accuracy: {accuracy * 100:.2f}%')

# Save your dynamically trained recommendation model (without encoding)
joblib.dump(model, 'models/merchant_recommendations_classifier.pkl')
print("Dynamic Merchant Recommendation Model saved clearly.")
