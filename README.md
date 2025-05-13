# DAG first approach

## 📌 Project Description

This project automates the extraction, transformation, and export of sales data from a PostgreSQL database, enhances the data with exchange rate information, and exports the results in CSV and Google Sheets formats. It uses a Directed Acyclic Graph (DAG) to manage task dependencies and execute them in order.

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

## 🛠️ Setup

### 1. Environment Variables:

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

### 2. Google Sheets Setup:

To export data to Google Sheets, you'll need to set up Google API credentials:

- Create a project in the Google Developers Console.

- Enable the "Google Sheets API" and "Google Drive API".

- Download the credentials JSON file and set the GOOGLE_CREDENTIALS_PATH in the .env file to the path of the credentials file.

## 👩‍💻 Author

Camila Javiera Muñoz Navarro
<br>

[LinkedIn](https://www.linkedin.com/in/camilajmn/) | [GitHub](https://github.com/CamilaJaviera91)

## 📄 License

This project is licensed under the MIT License.