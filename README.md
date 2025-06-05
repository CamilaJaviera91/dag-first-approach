# 💡 DAG-Based ETL Pipeline for Sales Reporting

## 🧠 Project Description:

This project automates the **extraction**, **transformation**, and **export** of sales data using `Apache Airflow`. It pulls **data** from a **PostgreSQL** database, enriches it with **USD to CLP exchange rate** information, and **exports** the final dataset to both a **CSV file** and a **Google Sheet**.

<br>

The **pipeline** is designed as a **Directed Acyclic Graph** (`DAG`) to manage task dependencies and ensure a reliable and repeatable workflow.

---

## 🚀 Project Structure:

```bash
dag-first-approach/
├── project_airflow_etl/
│   ├── config/
│   ├── dags/
│   │   └── etl_sales_report.py       # Airflow DAG definition
│   ├── data/
│   │   ├── report.csv                # Final report file
│   │   └── sales.png                 # Yearly sales
│   ├── logs/                         # Airflow logs
│   ├── plugins/                      # Custom Airflow plugins
│   ├── src/
│   │   └── etl_modules/              # ETL module scripts
│   │       ├── __init__.py
│   │       ├── connection.py
│   │       ├── enrich.py
│   │       ├── export.py
│   │       ├── extract.py
│   │       ├── generate_sales_plot.py
│   │       ├── google_sheets.py
│   │       └── usd_to_clp.py
│   ├── test/
│   │   ├── test_extract.py
│   │   ├── test_usd_to_clp.py
│   │   └── test_enrich.py
│   ├── airflow.cfg                   # Airflow configuration file
│   ├── airflow.db                    # Airflow database (SQLite for local use)
│   ├── docker-compose.yaml           # Docker setup for Airflow
│   ├── flask_session
│   ├── requirements.txt              # Python dependencies
└── README.md
```

---

## 🧩 What This Project Does?:

- **Extracts** data from a PostgreSQL database using a custom SQL query.

- **Fetches** the current USD to CLP exchange rate from a public API.

- **Enriches** the data by converting sales totals from USD to CLP.

- **Exports** the final dataset:

    - as a CSV file (`report.csv`)

    - to a Google Sheet

---

## 🛠️ Technologies Used:

- Python

- Apache Airflow

- PostgreSQL

- Google Sheets API

- Docker (via `docker-compose`)

- Pandas, Requests, Matplotlib

---

## 🗂️ What's DAG?:

A **Directed Acyclic Graph (DAG)** is a graph where:

1. **Directed:** All edges have a direction (from one node to another)

2. **Acyclic:** No cycles exist—you can’t loop back to a previous node

---

### 📋 Common Uses of DAGs:

- Task scheduling (e.g., Airflow, build systems like Make)

- Version control systems (`e.g., Git`)

- Data processing pipelines

- Compilers and expression trees

---

## 🚀 Installation and Execution:

1. Clone the repository:

```
git clone https://github.com/CamilaJaviera91/dag-first-approach.git
cd dag-first-approach
```

2. Create a Virtual Environment:

```
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Configure Environment Variables:

Create a `.env` file in the root directory and add the following:

```
DB_HOST=your_database_host
DB_PORT=your_database_port
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_SCHEMA=your_database_schema #optional

GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_SERVICE_ACCOUNT_FILE=path/to/your/service_account.json
```

5. Initialize the Airflow Database:

```
airflow db init
```

6. Set Up Google Sheets API

    - Follow this [guide](https://developers.google.com/workspace/sheets/api/quickstart/python?hl=es-419) to:

        1. Create a project in Google Developers Console.

        2. Enable the **Google Sheets API** and **Google Drive API**.

        3. Download the service account JSON credentials

        4. Set the path to this file in `GOOGLE_CREDENTIALS_PATH`.

    - Make sure to share your target Google Sheet with the service account email.

7. Run the main script:

```
python main.py
```

8. Start Postgres Services:

```
sudo systemctl start postgresql
```

9. Start Airflow Services:

```
airflow webserver --port 8080
airflow scheduler
```

10. Access the Airflow Web Interface:

Navigate to http://localhost:8080 in your web browser.

---

## 🧩 Sales ETL Pipeline

This project defines an Apache Airflow DAG that automates a complete ETL process:

- 📥 Extracts sales data from a PostgreSQL database.

- 💱 Fetches the current USD to CLP exchange rate.

- 🧪 Enriches the data by converting USD totals into CLP.

- 📊 Generates a sales plot by year.

- 💾 Exports the enriched data to a CSV file.

- ☁️ Sends the data to Google Sheets for easy access.

---
## ⚙️ DAG Task Flow

```
[A]📥Extract data ─> [B]💱Fetch rate ─> [C]🧪Enrich data
                                         ├─> [D]📊Generate sales plot
                                         ├───> [E]💾Export to CSV
                                         └─────> [F]☁️Export to Google Sheets
```

---

## 🗓️ DAG Configuration

| Parameter      | Value           |
| -------------- | --------------- |
| **DAG ID**     | `sales_etl_dag` |
| **Schedule**   | `@daily`        |
| **Catchup**    | `False`         |
| **Start Date** | `2024-01-01`    |
| **Owner**      | `Camila`        |

---

## ▶️ Execution Example:

- Run de pipeline: 

```
python dag_postgres.py
```

- You'll see output like:

```
✅ Successfully connected to PostgreSQL.
💱 Exchange rate: 1 USD = 900.50 CLP
📊 Enriched report:
📤 Exported report to 'report.csv'
📤 Data exported to Google Sheets: Sales Report -> ReportSheet
🔒 Connection closed successfully.
```

---

## 📊 Sample Output:

| year | store          | total       | total_clp     |
|------|----------------|-------------|---------------|
| 2020 | Teno-3	        |1,292,370.99 | 1,219,364,953 |
| 2020 | Cauquenes-5	|1,298,515.67 | 1,225,162,520 |
| 2020 | Villa Alegre-2	|1,325,040.86 | 1,250,189,302 |
| 2020 | Longaví-9      |1,353,795.29 | 1,277,319,394 |
| 2020 | Constitución-4 |1,353,981.94 | 1,277,495,500 |

---

## 📂 Output Files:

- results/report.csv

- Google Spreadsheet: `Sales Report → ReportSheet`

---

## ❗Troubleshooting:

- **Connection Errors:** Check your database credentials and network access.

- **Google Sheets Permissions:** Make sure the service account has access to edit the target sheet.

- **Missing Environment Variables:** Ensure `.env` is properly set and loaded.

---

## 📝 Notes:

- Ensure the database is accessible and credentials are valid

- The service account must have permission to edit the target Google Sheet

- You can customize the SQL query, filenames, and sheet names

---

## 📘 How to Add a DAG to Apache Airflow and Display It in the Webserver

Follow these steps to add your `DAG` to Apache Airflow and make it visible in the Airflow web interface.

1. 📂 **Place Your DAG in the dags Directory**

Airflow loads DAGs from a specific folder, typically located at:

```
~/airflow/dags/
```

- If you've changed the path in your `airflow.cfg` (`dags_folder`), use that custom directory instead.

2. 📝 **Create Your DAG File**

Create a new Python file inside the dags folder. For example:

```
~/airflow/dags/my_example_dag.py
```

3. 🔁 **Restart Airflow Services**

After placing your DAG file, restart the Airflow scheduler and webserver:

```
airflow scheduler
airflow webserver
```

4. 🌐 **Open the Airflow Web UI**

Visit the Airflow UI in your browser:

```
http://localhost:8080
```

- You should see your DAG (`my_example_dag`) listed. Enable it and trigger it as needed.

### 🛠️ Troubleshooting in how to Add a DAG to Apache Airflow

If your DAG doesn't appear:

- ✅ Ensure the file ends with .py

- ✅ Make sure dag_id is unique and the syntax is valid

- ✅ Confirm it's located in the correct dags_folder

- ✅ Check the Airflow scheduler logs for errors:

```
airflow scheduler --log-level INFO
```

---

## 🧪 Testing

This project uses `pytest` to validate the ETL modules and ensure they work as expected.

### ✅ How to Run Tests

- Run the tests:

```
pytest test/
```
This will execute all test files inside the `test/` folder.

- Results:

```
======================== test session starts ========================
platform linux -- Python 3.10.17, pytest-8.3.5, pluggy-1.6.0
rootdir: /home/user/dag-first-approach/project_airflow_etl
plugins: anyio-4.9.0
collected 3 items

test/test_enrich.py .                                          [ 33%]
test/test_extract.py .                                         [ 66%]
test/test_usd_to_clp.py  .                                     [100%]

========================= 3 passed in 2.19s =========================
```

### 📁 Example Test Structure

```
dag-first-approach/
├── src/
│   └── etl_modules/
├── test/
│   ├── test_extract.py
│   ├── test_usd_to_clp.py
│   └── test_enrich.py
```

---

## 🤝 Contributing:

Contributions are welcome! Please follow these steps:

- Fork the repository.

- Create a new branch: `git checkout -b feature/YourFeatureName`

- Commit your changes: `git commit -m 'Add some feature'`

- Push to the branch: `git push origin feature/YourFeatureName`

- Open a pull request.

---

## 📧 Questions?:

If you get stuck or need help customizing the pipeline, feel free to open an issue or reach out!

---

## 👩‍💻 Author:

**Camila Javiera Muñoz Navarro**  
[🔗 LinkedIn](https://www.linkedin.com/in/camilajmn/)  
[🐙 GitHub](https://github.com/CamilaJaviera91)

---

## 📄 License:

This project is licensed under the **MIT License**. 
