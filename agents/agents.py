from flask import Flask, jsonify, request
import psycopg2
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# ========================
# 🔌 DATABASE CONNECTION
# ========================
def get_db_connection():
    return psycopg2.connect(
        dbname="elderly_care",
        user="postgres",
        password="system",
        host="localhost",
        port="5432"
    )

# ========================
# 🏠 HOME ROUTE
# ========================
@app.route('/')
def home():
    return "👵👴 Welcome to Unified Elderly Care System API"

# ========================
# 🩺 HEALTH AGENT
# ========================
health_model = joblib.load('models/health_alert.pkl')

@app.route('/health', methods=['GET'])
def health_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM health_monitoring ORDER BY timestamp DESC LIMIT 10;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = [{
        'user_id': row[0],
        'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
        'heart_rate': row[2],
        'temperature': row[3],
        'bp_systolic': row[4],
        'bp_diastolic': row[5],
        'abnormal': bool(row[6])
    } for row in rows]

    return jsonify({'health_monitoring': result})

@app.route('/health/user/<user_id>', methods=['GET'])
def health_data_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM health_monitoring WHERE user_id = %s ORDER BY timestamp DESC LIMIT 1;", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "No health data found"}), 404

    result = {
        'user_id': row[0],
        'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
        'heart_rate': row[2],
        'temperature': row[3],
        'bp_systolic': row[4],
        'bp_diastolic': row[5],
        'abnormal': bool(row[6])
    }
    return jsonify({'health_monitoring': result})

@app.route('/health/predict', methods=['POST'])
def predict_health():
    data = request.get_json()
    input_df = pd.DataFrame([data])
    prediction = health_model.predict(input_df)
    return jsonify({'abnormal_prediction': int(prediction[0])})

@app.route('/health/auto_predict', methods=['POST'])
def auto_predict_health():
    data = request.get_json()
    user_id = data.get("user_id")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT heart_rate, temperature, bp_systolic, bp_diastolic
        FROM health_monitoring
        WHERE user_id = %s
        ORDER BY timestamp DESC LIMIT 1;
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        df = pd.DataFrame([{
            'heart_rate': row[0],
            'temperature': row[1],
            'bp_systolic': row[2],
            'bp_diastolic': row[3]
        }])
        prediction = health_model.predict(df)[0]
        return jsonify({"user_id": user_id, "abnormal_prediction": int(prediction)})
    else:
        return jsonify({"error": "No health data found"}), 404

# ========================
# 🛡️ SAFETY AGENT
# ========================
safety_model = joblib.load('models/safety_alert.pkl')

@app.route('/safety', methods=['GET'])
def safety_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM safety_monitoring ORDER BY timestamp DESC LIMIT 10;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = [{
        'user_id': row[0],
        'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
        'event_type': row[2],
        'location': row[3],
        'emergency_call': bool(row[4]),
        'unsafe': bool(row[5])
    } for row in rows]

    return jsonify({'safety_monitoring': result})

@app.route('/safety/user/<user_id>', methods=['GET'])
def safety_data_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM safety_monitoring 
        WHERE user_id = %s 
        ORDER BY timestamp DESC LIMIT 1;
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "No safety data found"}), 404

    result = {
        'user_id': row[0],
        'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
        'event_type': row[2],
        'location': row[3],
        'emergency_call': bool(row[4]),
        'unsafe': bool(row[5])
    }
    return jsonify({'safety_monitoring': result})

@app.route('/safety/predict', methods=['POST'])
def predict_safety():
    data = request.get_json()
    input_df = pd.DataFrame([data])
    prediction = safety_model.predict(input_df)
    return jsonify({'unsafe_prediction': int(prediction[0])})

@app.route('/safety/auto_predict', methods=['POST'])
def auto_predict_safety():
    data = request.get_json()
    user_id = data.get("user_id")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT event_type, location, emergency_call
        FROM safety_monitoring
        WHERE user_id = %s
        ORDER BY timestamp DESC LIMIT 1;
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        df = pd.DataFrame([{
            'event_type': row[0],
            'location': row[1],
            'emergency_call': row[2]
        }])
        prediction = safety_model.predict(df)[0]
        return jsonify({"user_id": user_id, "unsafe_prediction": int(prediction)})
    else:
        return jsonify({"error": "No safety data found"}), 404

# ========================
# ⏰ REMINDER AGENT
# ========================
reminder_model = joblib.load('models/daily_reminder.pkl')

@app.route('/reminders', methods=['GET'])
def reminders_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM daily_reminder ORDER BY timestamp DESC LIMIT 10;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = [{
        'user_id': row[0],
        'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
        'reminder_type': row[2],
        'start_time': str(row[3]),
        'schedule_time': str(row[3]),
        'reminder_sent': bool(row[4]),
        'acknowledged': bool(row[5])
    } for row in rows]

    return jsonify({'reminder_monitoring': result})

@app.route('/reminders/user/<user_id>', methods=['GET'])
def reminder_data_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM daily_reminder 
        WHERE user_id = %s 
        ORDER BY timestamp DESC LIMIT 1;
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "No reminders found"}), 404

    result = {
        'user_id': row[0],
        'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
        'reminder_type': row[2],
        'start_time': str(row[3]),
        'schedule_time': str(row[3]),
        'reminder_sent': bool(row[4]),
        'acknowledged': bool(row[5])
    }
    return jsonify({'daily_reminders': result})

@app.route('/reminders/predict', methods=['POST'])
def predict_reminder():
    data = request.get_json()
    input_df = pd.DataFrame([data])
    prediction = reminder_model.predict(input_df)
    return jsonify({'acknowledged_prediction': int(prediction[0])})

@app.route('/reminders/auto_predict', methods=['POST'])
def auto_predict_reminder():
    data = request.get_json()
    user_id = data.get("user_id")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT reminder_type, schedule_time
        FROM daily_reminder
        WHERE user_id = %s AND reminder_sent = TRUE
        ORDER BY timestamp DESC LIMIT 1;
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        df = pd.DataFrame([{
            'reminder_type': row[0],
            'schedule_time': row[1]
        }])
        prediction = reminder_model.predict(df)[0]
        return jsonify({"user_id": user_id, "acknowledged_prediction": int(prediction)})
    else:
        return jsonify({"error": "No reminders found"}), 404


# ========================
# Run the app
# ========================
if __name__ == '__main__':
    print("✅ API running on: http://127.0.0.1:5001")
    app.run(debug=True, port=5001)



'''
Agent	Endpoint
Health	http://127.0.0.1:5001/health
Safety	http://127.0.0.1:5001/safety
Reminder http://127.0.0.1:5001/reminders


'''