import networkx as nx
from faker import Faker
import pandas as pd
import random
import matplotlib.pyplot as plt

data_store = {}

def extract_data(n=1000):
    faker = Faker()
    products = ["Blue pen", "Red pen", "Black pen", "#2 Pencil", "Mechanical pencil", "Erasers", "Highlighter", "Colored pencils", 
                "markers", "Sharpener", "Lined notebooks or composition books", "Graph paper", "Loose-leaf paper", "Sticky notes", 
                "page flags", "3-ring binders", "Dividers with tabs", "Folder", "Index cards", "Pencil pouch", "Pencil case", "Clipboard", 
                "Ruler", "Protractor", "Compass", "Scientific calculator", "Graphing calculator", "Lab notebook", "USB flash drive", 
                "Laptop", "Tablet", "Headphones or earbuds", "Charger & extension cord", "Mouse", "Glue stick & liquid glue", 
                "Safety scissors", "Crayons or watercolor paints", "Construction paper", "Art sketchbook", "Water bottle", "Tissues", 
                "Hand sanitizer", "Backpack", "Lunch box or bag"]

    def generate_sales_data(n):
        sales = []
        for _ in range(n):
            product = random.choice(products)
            quantity = random.randint(12, 144) if random.random() > 0.05 else None
            unit_price = round(random.uniform(10.0, 500.0), 2) if random.random() > 0.05 else None
            date = faker.date_between(start_date='-1y', end_date='today')
            client = faker.company()
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
    duplicates = random.sample(records, k=int(n * 0.05))
    records.extend(duplicates)

    df = pd.DataFrame(records)
    data_store['raw'] = df
    df.to_csv("sales_unprocessed.csv", index=False)
    print("✅ Extracted data with simulated errors...")

def clean_data():
    df = data_store['raw'].copy()
    df['product'] = df['product'].str.strip()
    df['client'] = df['client'].str.strip()
    df = df.dropna()
    df = df.drop_duplicates()
    data_store['clean'] = df
    print("🧹 Cleaned data (whitespaces, nulls, duplicates)...")

def validate_data():
    df = data_store['clean']
    df = df[(df['quantity'] > 0) & (df['unit_price'] > 0)]
    data_store['validated'] = df
    print("✅ Validated data (positive quantity and price)...")

def transform_data():
    df = data_store['validated']
    df['total'] = df['quantity'] * df['unit_price']
    df['total'] = round(df['total'], 2)
    data_store['transformed'] = df
    print("🛠️ Transformed data...")

def analyze_data():
    df = data_store['transformed']
    top_products = df.groupby('product')['total'].sum().sort_values(ascending=False).head(5)
    print("🏆 Top 5 products by sales:")
    print(top_products)
    data_store['analysis'] = top_products

def plot_data():
    df = data_store['transformed']
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    monthly_sales = df.groupby('month')['total'].sum()
    monthly_sales.plot(kind='bar', figsize=(10, 5), title="Monthly Sales")
    plt.tight_layout()
    plt.savefig("monthly_sales.png")
    print("📊 Saved plot as 'monthly_sales.png'")

def load_data():
    df = data_store['transformed']
    df.to_csv("sales_processed.csv", index=False)
    print("📤 Data loaded into 'sales_processed.csv'.")

# DAG definition
tasks = {
    "extract": extract_data,
    "clean": clean_data,
    "validate": validate_data,
    "transform": transform_data,
    "analyze": analyze_data,
    "plot": plot_data,
    "load": load_data
}

dag = nx.DiGraph()
dag.add_edges_from([
    ("extract", "clean"),
    ("clean", "validate"),
    ("validate", "transform"),
    ("transform", "analyze"),
    ("transform", "plot"),
    ("transform", "load")
])

execution_order = list(nx.topological_sort(dag))
print("📋 Execution order:", execution_order)

for task in execution_order:
    tasks[task]()