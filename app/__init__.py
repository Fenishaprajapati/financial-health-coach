from flask import Flask
import os

# Get the absolute path of the templates folder to avoid any confusion
template_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=template_folder_path)

from app import routes
