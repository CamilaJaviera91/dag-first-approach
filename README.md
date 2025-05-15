# DAG first approach

## 📌 Project Description

This project automates the extraction, transformation, and export of sales data from a PostgreSQL database, enhances the data with exchange rate information, and exports the results in CSV and Google Sheets formats. It uses a Directed Acyclic Graph (DAG) to manage task dependencies and execute them in order.

---

## 🧩 What This Project Does

1. Extracts data from a PostgreSQL database using a custom SQL query.

2. Fetches the current USD to CLP exchange rate from a public API.

3. Enriches the data by converting sales totals from USD to CLP.

4. Exports the final dataset:

    - as a CSV file (report.csv)

    - to a Google Sheet

---

## 🗂️ What's DAG?

A DAG, or **Directed Acyclic Graph**, is a type of graph used in computer science and mathematics that has the following properties:

1. Directed: All edges (connections between nodes) have a direction — they go from one node to another in a specific direction.

2. Acyclic: There are no cycles — you can't start at one node and follow the edges to eventually loop back to the same node.

---

### 📋 Common Uses of DAGs:

- Task scheduling (e.g., Airflow, build systems like Make): Tasks depend on other tasks, and the execution order must follow the dependencies.

- Version control systems (e.g., Git): Commits are nodes in a DAG showing how changes depend on each other.

- Data processing pipelines: Stages of transformation that must occur in a specific order.

- Compilers: Representing expressions or instructions.

---

## ⚙️ Requirements

Before running the script, make sure you have the following dependencies installed:

```
pip install -r requirements.txt
```

---

## 🛠️ Setup

### 📖 1. Environment Variables:

The script uses environment variables to connect to the PostgreSQL database and authenticate with Google Sheets. Create a .env file in the project directory and include the following parameters:

```
DB_HOST=your_database_host
DB_PORT=your_database_port
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_SCHEMA=your_database_schema (optional)

GOOGLE_CREDENTIALS_PATH=path_to_your_google_credentials.json
```

### 📄 2. Google Sheets Setup:

To export data to Google Sheets, you'll need to set up Google API credentials:

- Create a project in the Google Developers Console.

- Enable the "Google Sheets API" and "Google Drive API".

- Download the credentials JSON file and set the GOOGLE_CREDENTIALS_PATH in the .env file to the path of the credentials file.

---

## 📝 Script Functions

### 1. connection()

Establishes a connection to the PostgreSQL database using the parameters from the .env file.

- **Returns:** conn (connection object), cur (cursor object) if successful, None, None if failed.

### 2. extract_data()

Extracts sales data from the PostgreSQL database by executing an SQL query that performs a series of joins and aggregations.

- **Returns:** A Pandas DataFrame containing the aggregated sales data.

### 3. fetch_usd_to_clp()

Fetches the current USD to CLP exchange rate from the ExchangeRate-API.

- **Returns:** The exchange rate (float) if successful, None if failed.

### 4. enrich_report()

Enriches the extracted data with the exchange rate (converts totals to CLP).

- **Parameters:**

    - **df_usd:** The DataFrame containing sales data in USD.

    - **clp_rate:** The exchange rate from USD to CLP.

- **Returns:** The enriched DataFrame with totals converted to CLP.

### 5. export_results()

Exports the enriched data to a CSV file (results/report.csv).

- **Parameters:**

    - **df:** The DataFrame containing the data to be exported.

- **Returns:** None.

### 6. export_to_google_sheets()

Exports the enriched data to a Google Sheet using the Google Sheets API.

- **Parameters:**

    - **df:** The DataFrame containing the data to be exported.

    - **sheet_name:** The name of the sheet within the spreadsheet.

    - **spreadsheet_name:** The name of the spreadsheet.

- **Returns:** None.

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

1. extract (Extract data from PostgreSQL)

2. fetch_usd_to_clp (Fetch exchange rate)

3. enrich_report (Enrich data with exchange rate)

4. export (Export to CSV)

5. googlesheets (Export to Google Sheets)

---

## ▶️ Execution Example

To run the script, execute the Python file directly:

```
python dag_postgres.py
```

The tasks will be executed in the order defined by the DAG, and the enriched sales data will be saved to both a CSV file and a Google Sheet.

---

## 📝 Notes

- Make sure your PostgreSQL database is accessible, and your Google API credentials are set up correctly.

- The Google Sheets API requires the appropriate permissions to modify the sheet, so ensure your service account has the necessary access.

---

## 👩‍💻 Author

Camila Javiera Muñoz Navarro
<br>

[LinkedIn](https://www.linkedin.com/in/camilajmn/) | [GitHub](https://github.com/CamilaJaviera91)

---

## 📄 License

This project is licensed under the MIT License.