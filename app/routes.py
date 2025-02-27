import os
from flask import render_template, request
import pandas as pd
from app import app
from app.utils import process_data

# Home route (file upload)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        
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
            processed_data = process_data(data)  # Process the data

            # Convert the processed DataFrame to an HTML table
            tables = processed_data.to_html(classes='data', index=False)

            # Clean up the table string to remove unwanted characters
            tables = tables.replace('\n', '')  # Remove newline characters

            # Render the dashboard with processed data
            return render_template("dashboard.html", tables=tables, titles=[""])

    return render_template("index.html")
