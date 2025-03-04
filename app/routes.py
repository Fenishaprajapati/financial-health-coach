from flask import Flask, render_template, request
import pandas as pd
from app import app
import os
from app.utils import predict_category, check_budget_spending, standardize_columns  # Import the function from utils.py

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        file = request.files['file']

        # Ensure the 'uploads' directory exists
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Save the uploaded CSV file
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Read the CSV file
        data = pd.read_csv(file_path)

        # Standardize the column names
        try:
            data = standardize_columns(data)
        except ValueError as e:
            return str(e)  # If columns are not found, show the error message

        # Apply model-based category prediction
        data['Category'] = data['Merchant'].apply(lambda x: predict_category(x))

        # Summarize the data by merchant and category
        brand_category_summary = data.groupby(['Merchant', 'Category'])['Amount'].sum().reset_index()

        # Summarize overall spending by category
        overall_spending = data.groupby('Category')['Amount'].sum().reset_index()

        # Retrieve budget goals from the form
        budget_goals = {
            "Groceries": float(request.form.get("groceries", 0)),
            "Transport": float(request.form.get("transport", 0)),
            "Food & Drink": float(request.form.get("food", 0)),
            "Entertainment": float(request.form.get("entertainment", 0)),
            "Shopping": float(request.form.get("Shopping", 0)),
            "Utilities & Bills": float(request.form.get("Utilities & Bills", 0)),
            "Mobile Services": float(request.form.get("Mobile Services", 0)),
        }

        # Check if the user is within budget or not, and generate alerts
        alerts = check_budget_spending(overall_spending, budget_goals)

        # Render the dashboard with summarized data and alerts
        return render_template("dashboard.html", 
                               brand_category_summary=brand_category_summary, 
                               overall_spending=overall_spending, 
                               alerts=alerts)

    return render_template("index.html")
