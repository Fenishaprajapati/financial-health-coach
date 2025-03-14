from flask import Flask, render_template, request
import pandas as pd
import os
from app import app
from app.utils import (
    predict_category, 
    recommend_alternative_merchant, 
    standardize_columns, 
    check_budget_alerts
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files['file']

        # ensure uploads directory exists
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # save the uploaded file
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # read and standardize CSV file
        data = pd.read_csv(file_path)
        data = standardize_columns(data)

        # predict spending categories
        data['Category'] = data['Merchant'].apply(predict_category)

        # define budgets from user input clearly
        budget_goals = {
            "Groceries": float(request.form.get("groceries", 0)),
            "Transport": float(request.form.get("transport", 0)),
            "Food & Drink": float(request.form.get("food", 0)),
            "Entertainment": float(request.form.get("entertainment", 0)),
            "Shopping": float(request.form.get("shopping", 0)),
            "Utilities & Bills": float(request.form.get("Utilities & Bills", 0)),
            "Mobile Services": float(request.form.get("Mobile Services", 0)),
        }

        # generate budget alerts clearly
        alerts, overspent_categories = check_budget_alerts(data, budget_goals)

        # summarize data
        brand_category_summary = data.groupby(['Merchant', 'Category'], as_index=False)['Amount'].sum()
        overall_spending = data.groupby('Category')['Amount'].sum().reset_index()

        # generate alternative recommendations ONLY for merchants causing overspending
        overspent_merchants = data[data['Category'].isin(overspent_categories)]['Merchant'].unique()

        recommendations = []
        for merchant in overspent_merchants:
            alternative = recommend_alternative_merchant(merchant)
            recommendations.append({"Merchant": merchant, "Alternative Recommendation": alternative})

        recommendations_df = pd.DataFrame(recommendations)

        return render_template(
            "dashboard.html",
            brand_category_summary=brand_category_summary,
            overall_spending=overall_spending,
            alerts=alerts,
            alternative_recommendations=recommendations_df
        )

    return render_template("index.html")
