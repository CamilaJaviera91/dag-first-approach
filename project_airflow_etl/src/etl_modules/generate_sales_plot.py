import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

def generate_sales_by_year_plot(data: list[dict], output_path: str = 'data/yearly_sales.png'):
    df = pd.DataFrame(data)

    if 'year' not in df.columns or 'total_clp' not in df.columns:
        raise ValueError("Missing required columns in data: 'Year' and 'total_clp'.")

    df['year'] = df['year'].astype(int)
    df['total_clp'] = pd.to_numeric(df['total_clp'])

    sales = df.groupby('year')['total_clp'].sum().reset_index()

    plt.figure(figsize=(8, 5))
    plt.bar(sales['year'], sales['total_clp'], color='skyblue')
    plt.title('Total de Ventas Anuales en CLP')
    plt.xlabel('Year')
    plt.ylabel('Total CLP')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(sales['year'])
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()