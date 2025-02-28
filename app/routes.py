from flask import render_template, request
import pandas as pd
from app import app

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle CSV file upload and budget goal form submission
        pass

    return render_template("index.html")
