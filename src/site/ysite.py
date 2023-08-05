from flask import Flask, render_template, request, redirect

import sqlite3
import sys

import sys
sys.path.append('C:\\Users\\Vinea\\Desktop\\Personal Projects\\ybot\\src')
from utils.utility import Utility

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
    # return render_template("index.html", name=name)
    return redirect("https://www.google.com/")
@app.route("/e")
def code():
    name = request.args.get("code")

    print(f'code: {name}')
    # we need to store the code in a database which can be accessed in testy.py
    """code here"""
    if name is not None:
        u.register(name)

    print(f'Code: {name}')
    return "<h1>yo</h1>"

app.run()