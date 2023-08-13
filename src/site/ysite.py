from flask import Flask, render_template, request, redirect
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR Site: {project_root}")
sys.path.append(project_root)
from src.utils.utility import Utility

u = Utility()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/e")
def code():
    code = request.args.get("code")
    if code is not None:
        try:
            u.register(code)
            print("Successfully registered")
            return render_template('index.html')
        except Exception as e:
            print(e)
            print("Failed to register")
            return redirect("https://www.google.com/")
    return render_template('index.html')

app.run()