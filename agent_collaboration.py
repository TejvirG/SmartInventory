import pandas as pd
from ollama_interface import query_mistral

class StoreAgent:
    def __init__(self, store_id, stock_df):
        self.store_id = store_id
        self.stock_df = stock_df

    def check_stock(self, threshold=10):
        return self.stock_df[
            (self.stock_df['Store ID'] == self.store_id) &
            (self.stock_df['Stock Levels'] < threshold)
        ]

    def request_restock(self, product_id, quantity):
        return {"store_id": self.store_id, "product_id": product_id, "quantity": quantity}

class WarehouseAgent:
    def __init__(self, inventory_df):
        self.inventory_df = inventory_df

    def fulfill_request(self, restock_request):
        product = restock_request['product_id']
        quantity = restock_request['quantity']
        available = self.inventory_df.loc[
            self.inventory_df['Product ID'] == product, 'Stock Levels'
        ].sum()

        if available >= quantity:
            return f"Request fulfilled for {product} - Qty: {quantity}"
        else:
            return f"Insufficient stock for {product}"

class SupplierAgent:
    def __init__(self, lead_times_df):
        self.lead_times_df = lead_times_df

    def order_stock(self, product_id, quantity):
        lead_time = self.lead_times_df.loc[
            self.lead_times_df['Product ID'] == product_id,
            'Supplier Lead Time (days)'
        ].values[0]
        return f"Order placed for {quantity} units of {product_id}. Estimated delivery in {lead_time} days."

class CustomerAgent:
    def __init__(self, demand_data):
        self.demand_data = demand_data

    def get_demand_trend(self, product_id):
        product_data = self.demand_data[self.demand_data['Product ID'] == product_id]
        if len(product_data) < 7:
            return "Not enough data to calculate trend"
        return product_data['Sales Quantity'].rolling(7).mean().iloc[-1]

def run_multiagent_simulation():
    inventory_df = pd.read_csv("inventory_monitoring.csv")
    inventory_df.columns = inventory_df.columns.str.strip()

    pricing_df = pd.read_csv("pricing_optimization.csv")
    pricing_df.columns = pricing_df.columns.str.strip()

    demand_df = pd.read_csv("demand_forecasting.csv")
    demand_df.columns = demand_df.columns.str.strip()

    store = StoreAgent(store_id=1, stock_df=inventory_df)
    warehouse = WarehouseAgent(inventory_df=inventory_df)
    supplier = SupplierAgent(lead_times_df=inventory_df)
    customer = CustomerAgent(demand_data=demand_df)

    low_stock_items = store.check_stock()
    restock_responses = []

    for _, row in low_stock_items.iterrows():
        product_id = row['Product ID']
        restock_request = store.request_restock(product_id, quantity=20)

        warehouse_response = warehouse.fulfill_request(restock_request)

        if "Insufficient" in warehouse_response:
            supplier_response = supplier.order_stock(product_id, quantity=20)
        else:
            supplier_response = "No need to reorder from supplier."

        demand_trend = customer.get_demand_trend(product_id)

        insight_prompt = f"""Given the product ID {product_id}, warehouse status: "{warehouse_response}", and demand trend: "{demand_trend}", generate an intelligent inventory decision or insight for the store manager."""
        mistral_response = query_mistral(insight_prompt)

        restock_responses.append({
            "Product ID": product_id,
            "Store ID": store.store_id,
            "Restock Request": restock_request,
            "Warehouse Response": warehouse_response,
            "Supplier Response": supplier_response,
            "Customer Demand Trend": demand_trend,
            "Mistral Insight": mistral_response
        })

    df_output = pd.DataFrame(restock_responses)
    df_output.to_csv("agent_collaboration_output.csv", index=False)
    return df_output
