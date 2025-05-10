import networkx as nx
from faker import Faker
import pandas as pd
import random

data_store = {}

def extract_data(n=1000):
    faker = Faker()
    products = ['item1', 'item2', 'item3', 'item4']

    def generate_sales_data(n):
        sales = []
        for _ in range(n):
            product = random.choice(products)
            # Randomly introduce null values
            quantity = random.randint(12, 144) if random.random() > 0.05 else None
            unit_price = round(random.uniform(10.0, 500.0), 2) if random.random() > 0.05 else None
            date = faker.date_between(start_date='-1y', end_date='today')
            client = faker.company()
            # Add random whitespaces
            if random.random() < 0.1:
                client = f"  {client}  "
            if random.random() < 0.1:
                product = f"  {product}  "
            sales.append({
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "date": date,
                "client": client
            })
        return sales

    records = generate_sales_data(n)

    # Intentionally duplicate some records
    duplicates = random.sample(records, k=int(n * 0.05))
    records.extend(duplicates)

    df = pd.DataFrame(records)
    data_store['raw'] = df
    print("✅ Extracted data with simulated errors...")

def clean_data():
    df = data_store['raw'].copy()
    
    # Strip leading/trailing whitespaces
    df['product'] = df['product'].str.strip()
    df['client'] = df['client'].str.strip()

    # Drop nulls
    df = df.dropna()

    # Drop duplicates
    df = df.drop_duplicates()

    data_store['clean'] = df
    print("🧹 Cleaned data (whitespaces, nulls, duplicates)...")

def transform_data():
    df = data_store['clean']
    df['total'] = df['quantity'] * df['unit_price']
    data_store['transformed'] = df
    print("🛠️ Transformed data...")

def load_data():
    df = data_store['transformed']
    df.to_csv("sales_processed.csv", index=False)
    print("📤 Data loaded into 'sales_processed.csv'.")

# DAG definition
tasks = {
    "extract": extract_data,
    "clean": clean_data,
    "transform": transform_data,
    "load": load_data
}

dag = nx.DiGraph()
dag.add_edges_from([
    ("extract", "clean"),
    ("clean", "transform"),
    ("transform", "load")
])

execution_order = list(nx.topological_sort(dag))
print("📋 Execution order:", execution_order)

for task in execution_order:
    tasks[task]()