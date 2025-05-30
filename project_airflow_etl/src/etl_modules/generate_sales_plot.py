import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def generate_sales_by_year_plot(data: list[dict], output_path: str):

    df = pd.DataFrame(data)

    if 'Year' not in df.columns or 'total_clp' not in df.columns:
        raise ValueError("Missing required columns in data: 'Year' and 'total_clp'.")

    df['Year'] = df['Year'].astype(int)
    df['total_clp'] = pd.to_numeric(df['total_clp'])

    sales = df.groupby('Year')['total_clp'].sum().reset_index()

    plt.figure(figsize=(8, 5))
    plt.bar(sales['Year'], sales['total_clp'], color='skyblue')
    plt.title('Total de Ventas Anuales en CLP')
    plt.xlabel('Año')
    plt.ylabel('Total CLP')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(sales['Year'])
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()