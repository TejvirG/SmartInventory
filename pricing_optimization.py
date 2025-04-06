import pandas as pd
from ollama_interface import get_mistral_insight

def optimize_pricing(file_path="pricing_optimization.csv"):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    df['Adjusted Price'] = df['Price']
    low_sales = df['Sales Volume'] < df['Sales Volume'].mean()
    high_price = df['Price'] > df['Price'].mean()
    df.loc[low_sales & high_price, 'Adjusted Price'] *= 0.95

    summary_prompt = f"Here is the pricing data:\n{df[['Product ID', 'Price', 'Sales Volume', 'Adjusted Price']].head(10).to_string()}\nExplain the pricing strategy."
    insight = get_mistral_insight(summary_prompt)

    return df[['Product ID', 'Store ID', 'Price', 'Adjusted Price']], insight
