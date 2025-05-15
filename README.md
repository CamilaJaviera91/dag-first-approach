# 💡 DAG-Based ETL Pipeline for Sales Reporting

## 📌 Project Description

This project automates the extraction, transformation, and export of sales data from a PostgreSQL database. It enriches the data with real-time USD to CLP exchange rate information and exports the results to both CSV and Google Sheets formats. A Directed Acyclic Graph (DAG) is used to manage task dependencies and ensure the correct execution order.

---

## 🧩 What This Project Does

- Extracts data from a PostgreSQL database using a custom SQL query.

- Fetches the current USD to CLP exchange rate from a public API.

- Enriches the data by converting sales totals from USD to CLP.

- Exports the final dataset:

    - as a CSV file (report.csv)

    - to a Google Sheet

---

## 🗂️ What's DAG?

A Directed Acyclic Graph (DAG) is a graph where:

- Directed: All edges have a direction (from one node to another)

- Acyclic: No cycles exist—you can’t loop back to a previous node

---

### 📋 Common Uses of DAGs:

- Task scheduling (e.g., Airflow, build systems like Make)

- Version control systems (e.g., Git)

- Data processing pipelines

- Compilers and expression trees

---

## ⚙️ Requirements

Before running the script, make sure you have the following dependencies installed:

```
pip install -r requirements.txt
```

---

## 🛠️ Setup

### 🔐 1. Environment Variables:

Create a `.env` file with the following:

```
DB_HOST=your_database_host
DB_PORT=your_database_port
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_SCHEMA=your_database_schema #optional

GOOGLE_CREDENTIALS_PATH=path_to_your_google_credentials.json
```

### 📄 2. Google Sheets Setup:

1. Create a project in Google Developers Console.

2. Enable the **Google Sheets API** and **Google Drive API**.

3. Download the JSON credentials file.

5. Set the path to this file in `GOOGLE_CREDENTIALS_PATH`.

---

## 📝 Script Functions

**1. connection()**

Establishes a connection to the PostgreSQL database.

    - Returns: conn, cur on success; None, None on failure

**2. extract_data()**

Runs an SQL query to extract and aggregate sales data.

    - Returns: DataFrame of extracted data

**3. fetch_usd_to_clp()**

Fetches the current USD to CLP exchange rate.

    - Returns: float (exchange rate) or None on failure

**4. enrich_report(df_usd, clp_rate)**

Adds a CLP total to the report using the fetched exchange rate.

    - Returns: Enriched DataFrame

**5. export_results(df)**

Saves the enriched data as `results/report.csv`

**6. export_to_google_sheets(df, sheet_name, spreadsheet_name)**

Exports the data to a `Google Sheet`

---

## 📑 Task Execution Flow

- **Data Extraction:** The script starts by extracting the data from the PostgreSQL database using the extract_data() function.

- **Exchange Rate Fetch:** The script fetches the USD to CLP exchange rate using the fetch_usd_to_clp() function.

- **Report Enrichment:** The sales data is enriched by converting the totals to CLP using the exchange rate.

- **CSV Export:** The enriched report is exported to a CSV file.

- **Google Sheets Export:** Finally, the enriched report is exported to a Google Sheet.

---

## 🔁 DAG (Directed Acyclic Graph)

A Directed Acyclic Graph (DAG) is used to define task dependencies and ensure they are executed in the correct order:

```
dag = nx.DiGraph()
dag.add_edges_from([
    ("extract", "fetch_usd_to_clp"),
    ("fetch_usd_to_clp", "enrich_report"),
    ("enrich_report", "export"),
    ("export", "googlesheets"),
])
```

---

## ⏩ Execution Order

The tasks are executed in the following order:

1. `extract` (Extract data from PostgreSQL)

2. `fetch_usd_to_clp` (Fetch exchange rate)

3. `enrich_report` (Enrich data with exchange rate)

4. `export` (Export to CSV)

5. `googlesheets` (Export to Google Sheets)

---

## ▶️ Execution Example

- To run the script, execute the Python file directly:

```
python dag_postgres.py
```

- The tasks will be executed in the order defined by the DAG, and the enriched sales data will be saved to both a CSV file and a Google Sheet.

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

## 📂 Output Files

- results/report.csv

- Google Spreadsheet: Sales Report → ReportSheet

---

## 📝 Notes

- Make sure your PostgreSQL database is accessible, and your Google API credentials are set up correctly.

- The Google Sheets API requires the appropriate permissions to modify the sheet, so ensure your service account has the necessary access.

- You can change the SQL query or sheet names as needed.

---

## 📧 Questions?

If you get stuck or need help customizing the pipeline, feel free to open an issue or reach out!

---

## 👩‍💻 Author

**Camila Javiera Muñoz Navarro**  
[🔗 LinkedIn](https://www.linkedin.com/in/camilajmn/)  
[🐙 GitHub](https://github.com/CamilaJaviera91)

---

## 📄 License

This project is licensed under the MIT License.