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
    return redirect("https://www.google.com/")

@app.route("/e")
def code():
    name = request.args.get("code")
    if name is not None:
        try:
            u.register(name)
            return "<h1>Successfully registered</h1>"
        except Exception as e:
            print(e)
            return "<h1>Failed to register</h1>"
    return """<head><title>Hi!</title></head>
            <h1>Welcome!</h1>"""

app.run()