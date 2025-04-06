from flask import Flask, jsonify
import psycopg2
import datetime

app = Flask(__name__)

# Connect to PostgreSQL once
conn = psycopg2.connect(
    dbname="elderly_care",
    user="postgres",
    password="system",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

@app.route("/")
def home():
    return jsonify({"message": "Elderly Care Multi-Agent API is running!"})

# Health Monitoring Endpoint
@app.route("/health", methods=["GET"])
def get_health_data():
    cur.execute("SELECT * FROM health_monitoring")
    data = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    result = []
    for row in data:
        row_dict = {}
        for key, value in zip(columns, row):
            row_dict[key] = str(value)
        result.append(row_dict)

    return jsonify({"health_monitoring": result})


# Daily Reminders Endpoint
@app.route("/reminders", methods=["GET"])
def get_reminders():
    cur.execute("SELECT * FROM daily_reminder")
    data = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    result = []
    for row in data:
        row_dict = {}
        for key, value in zip(columns, row):
            if isinstance(value, (datetime.time, datetime.date)):
                value = str(value)
            row_dict[key] = value
        result.append(row_dict)

    return jsonify({'daily_reminders': result})


# Safety Monitoring Endpoint
@app.route("/safety", methods=["GET"])
def get_safety_data():
    cur.execute("SELECT * FROM safety_monitoring")
    data = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    result = []
    for row in data:
        row_dict = {}
        for key, value in zip(columns, row):
            row_dict[key] = str(value)
        result.append(row_dict)

    return jsonify({"safety_monitoring": result})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
