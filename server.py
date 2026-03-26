from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running ✅"

@app.route("/query")
def query():
    return {"data": []}

@app.route("/data", methods=["POST"])
def data():
    return {"success": True}
