import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
import joblib

# Load synthetic dataset
df = pd.read_csv('data/synthetic_transactions_300.csv')

# Extract features (Merchant names) and labels (Categories)
X = df['Merchant']
y = df['Category']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a machine learning pipeline: TF-IDF vectorizer + Naive Bayes classifier
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

# Save the trained model to disk
joblib.dump(model, 'models/merchant_classifier.pkl')
print("Model saved as 'merchant_classifier.pkl'")
  



         