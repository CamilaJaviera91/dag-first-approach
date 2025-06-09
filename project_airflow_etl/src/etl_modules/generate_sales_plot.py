import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def generate_sales_by_year_plot(data: list[dict], output_path: str = 'data/yearly_sales.png'):
    if not data:
        raise ValueError("Input data is empty.")

    # Verificar columnas requeridas antes de crear el DataFrame
    all_keys = set().union(*(d.keys() for d in data))
    required_columns = {'year', 'total_clp'}
    missing_columns = required_columns - all_keys
    if missing_columns:
        raise ValueError(f"Missing required columns in data: {missing_columns}.")

    df = pd.DataFrame(data)

    if df[['year', 'total_clp']].isnull().any().any():
        raise ValueError("Null values found in required columns: 'year' and/or 'total_clp'.")

    df_grouped = df.groupby('year')['total_clp'].sum().reset_index()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.bar(df_grouped['year'], df_grouped['total_clp'], color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Total CLP')
    plt.title('Total Sales by Year (CLP)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()