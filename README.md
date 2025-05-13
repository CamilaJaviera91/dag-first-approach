# DAG first approach

## 📌 Project Description

This project automates the extraction, transformation, and export of sales data from a PostgreSQL database, enhances the data with exchange rate information, and exports the results in CSV and Google Sheets formats. It uses a Directed Acyclic Graph (DAG) to manage task dependencies and execute them in order.

## 🛠️ Technologies Used

- Python 3.10+
- Apache Airflow 2.7+
- Docker & Docker Compose (for local deployment)
- Virtualenv (optional)

## What's DAG?

A DAG, or **Directed Acyclic Graph**, is a type of graph used in computer science and mathematics that has the following properties:

1. Directed: All edges (connections between nodes) have a direction — they go from one node to another in a specific direction.

2. Acyclic: There are no cycles — you can't start at one node and follow the edges to eventually loop back to the same node.

### Common Uses of DAGs:

- Task scheduling (e.g., Airflow, build systems like Make): Tasks depend on other tasks, and the execution order must follow the dependencies.

- Version control systems (e.g., Git): Commits are nodes in a DAG showing how changes depend on each other.

- Data processing pipelines: Stages of transformation that must occur in a specific order.

- Compilers: Representing expressions or instructions.

## 📅 DAG Overview

- start_task: Dummy operator to signal the start of the DAG

- extract_data: Simulates data extraction

- transform_data: Simulates data transformation

- load_data: Simulates loading data into a target system

All tasks are executed sequentially to demonstrate dependency chaining.

## 👩‍💻 Author

Camila Javiera Muñoz Navarro
<br>

[LinkedIn](https://www.linkedin.com/in/camilajmn/) | [GitHub](https://github.com/CamilaJaviera91)

## 📄 License

This project is licensed under the MIT License.