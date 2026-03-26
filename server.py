from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

file_index = 1
row_count = 0
file_name = f"data_{file_index}.csv"

if not os.path.exists(file_name):
    with open(file_name, "w") as f:
        f.write("distance_cm,level_percent\n")

@app.route("/data", methods=["POST"])
def receive_data():
    global row_count, file_index, file_name

    data = request.get_json()

    distance = data.get("distance_cm")
    level = data.get("level_percent")

    with open(file_name, "a") as f:
        f.write(f"{distance},{level}\n")

    row_count += 1

    if row_count >= 24:
        file_index += 1
        file_name = f"data_{file_index}.csv"
        with open(file_name, "w") as f:
            f.write("distance_cm,level_percent\n")
        row_count = 0

    return jsonify({"success": True})

@app.route("/query", methods=["GET"])
def get_data():
    result = []

    for file in os.listdir():
        if file.endswith(".csv"):
            with open(file, "r") as f:
                lines = f.readlines()[1:]

                for line in lines:
                    if line.strip():
                        d, l = line.strip().split(",")
                        result.append({
                            "distance": float(d),
                            "level": float(l)
                        })

    return jsonify(result)
