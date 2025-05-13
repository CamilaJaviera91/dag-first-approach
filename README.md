# DAG first approach

This repository contains a simple example of an Apache Airflow DAG ("Directed Acyclic Graph") for orchestration of a basic data pipeline. It is intended as a starting point for understanding how to define, schedule, and run tasks using Airflow.

## 📌 Project Description

The goal of this project is to provide a minimal and clear setup to get started with Airflow DAGs. It includes:

- A basic DAG with Python tasks
- Task dependencies and execution order
- Local development setup instructions

This project follows a "DAG-first" development approach: you start by defining your DAG structure and logic before integrating it into a larger pipeline system.

## 🛠 Technologies Used

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

## 👩‍💻 Author

Camila Javiera Muñoz Navarro

<br>

[LinkedIn](https://www.linkedin.com/in/camilajmn/) | [GitHub](https://github.com/CamilaJaviera91)