import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

def generate_sales_by_year_plot(data: list[dict], output_path: str = 'data/yearly_sales.png'):
    df = pd.DataFrame(data)

    required_columns = {'year', 'total_clp'}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns in data: {missing_columns}.")

    if df[['year', 'total_clp']].isnull().any().any():
        raise ValueError("Null values found in required columns: 'year' and/or 'total_clp'.")

    df['year'] = df['year'].astype(int)
    df['total_clp'] = df['total_clp'].astype(float)

    df = df.sort_values('year')

    plt.figure(figsize=(10, 6))
    plt.bar(df['year'], df['total_clp'])
    plt.xlabel('Year')
    plt.ylabel('Total Sales (CLP)')
    plt.title('Total Sales by Year in CLP')
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()