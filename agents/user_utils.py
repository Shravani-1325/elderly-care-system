import psycopg2

def get_user_ids():
    conn = psycopg2.connect(
        host="localhost",
        database="elderly_care",
        user="postgres",
        password="system",
        port=5432
    )
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT user_id FROM health_monitoring ORDER BY user_id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row[0] for row in rows]
