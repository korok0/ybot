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
def hello_world():
    return redirect("https://www.google.com/")

@app.route("/route1")
def route_one():
    name = request.args.get("name")
    print(name)
    if name is None:
        name = "Friend"
    return redirect("https://www.google.com/")

@app.route("/e")
def code():
    name = request.args.get("code")
    if name is not None:
        u.register(name)
    return "<h1>yo</h1>"

app.run()