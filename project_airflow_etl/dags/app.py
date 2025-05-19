# airflow webserver --port 8080

from flask import Flask, jsonify
from etl_sales_report import dag

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Sales Report Application!"

@app.route('/run_etl')
def run_etl():
    # Here you can execute your DAG or specific ETL functions
    # For example:
    # dag.run()
    return "ETL executed successfully"

if __name__ == '__main__':
    app.run(debug=True)
