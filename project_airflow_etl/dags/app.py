from flask import Flask, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Airflow REST API endpoint
AIRFLOW_API_URL = 'http://localhost:8080/api/v1/dags/sales_etl_dag/dagRuns'
AIRFLOW_USER = 'your_airflow_username'
AIRFLOW_PASSWORD = 'your_airflow_password'

@app.route('/')
def home():
    return "Welcome to the Sales Report Application!"

@app.route('/trigger_etl', methods=['POST'])
def trigger_etl():
    """Trigger the Airflow DAG"""
    response = requests.post(
        AIRFLOW_API_URL,
        auth=HTTPBasicAuth(AIRFLOW_USER, AIRFLOW_PASSWORD),
        json={"conf": {"key": "value"}}  # Optional: pass parameters to your DAG
    )
    if response.status_code == 200:
        return jsonify({"message": "ETL process triggered successfully!"}), 200
    else:
        return jsonify({"error": "Failed to trigger ETL process", "details": response.text}), 500

if __name__ == '__main__':
    app.run(debug=True)
