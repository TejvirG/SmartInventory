import pandas as pd
from ollama_interface import get_mistral_insight

def identify_low_inventory(file_path="inventory_monitoring.csv", threshold=20):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    if 'Inventory' in df.columns:
        low_inventory = df[df["Inventory"] < threshold]
    elif 'Stock Levels' in df.columns:
        low_inventory = df[df["Stock Levels"] < threshold]
    else:
        raise ValueError("Expected 'Inventory' or 'Stock Levels' column in inventory file.")
    
    return low_inventory
