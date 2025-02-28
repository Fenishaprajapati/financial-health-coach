from flask import render_template, request
import pandas as pd
from app import app
import os
from app.utils import process_data, check_budget_spending  # Importing from utils.py

# Home route (file upload and budget goals form)
@app.route("/", methods=["GET", "POST"])
def index():
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'index.html')
    print(f"Template path: {template_path}")
    if not os.path.exists(template_path):
        print("index.html not found!")
    else:
        print("index.html found!")
        
    if request.method == "POST":
        # Handle CSV file upload
        file = request.files['file']

        # Retrieve budget goals from the form
        budget_goals = {
            "Groceries": float(request.form["groceries"]),
            "Transport": float(request.form["transport"]),
            "Food & Drink": float(request.form["food"]),
            "Entertainment": float(request.form["entertainment"]),
            "Shopping": float(request.form["Shopping"]),
            "Utilities & Bills": float(request.form["Utilities & Bills"]),
            "Mobile Services": float(request.form["Mobile Services"]),
        }

        # Ensure the 'uploads' directory exists
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        if file and file.filename.endswith('.csv'):
            # Save the uploaded file to the 'uploads' directory
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)

            # Read and process the CSV file
            data = pd.read_csv(file_path)
            
            # Process the data to handle dynamic columns
            brand_category_summary, overall_spending = process_data(data)

            # Convert the processed DataFrame to an HTML table
            brand_category_table = brand_category_summary.to_html(classes='data', index=False)
            overall_table = overall_spending.to_html(classes='data', index=False)

            # Check for budget alerts (use function we defined earlier)
            alerts = check_budget_spending(overall_spending, budget_goals)

            return render_template("dashboard.html", 
                                   brand_category_table=brand_category_table, 
                                   overall_table=overall_table, 
                                   alerts=alerts)

    return render_template("templates/index.html")
