# DAG first approach

## What's DAG?

A DAG, or **Directed Acyclic Graph**, is a type of graph used in computer science and mathematics that has the following properties:

1. Directed: All edges (connections between nodes) have a direction — they go from one node to another in a specific direction.

2. Acyclic: There are no cycles — you can't start at one node and follow the edges to eventually loop back to the same node.

### Common Uses of DAGs:

- Task scheduling (e.g., Airflow, build systems like Make): Tasks depend on other tasks, and the execution order must follow the dependencies.

- Version control systems (e.g., Git): Commits are nodes in a DAG showing how changes depend on each other.

- Data processing pipelines: Stages of transformation that must occur in a specific order.

- Compilers: Representing expressions or instructions.