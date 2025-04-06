import streamlit as st
import pandas as pd

from demand_forecasting import forecast_demand
from inventory_monitoring import identify_low_inventory
from pricing_optimization import optimize_pricing
from agent_collaboration import run_multiagent_simulation
from ollama_interface import get_mistral_insight

st.set_page_config(page_title="Retail Inventory Optimization", layout="wide")
st.title("Retail Inventory Optimization with Multi-Agent AI System")

# Demand Forecasting Section
st.header("Demand Forecasting")
forecast, summary = forecast_demand("demand_forecasting.csv")
forecast_df = pd.DataFrame({"Forecasted Demand": forecast})

st.write("Forecasted Demand:")
st.dataframe(forecast_df)
st.write("Mistral Insight:")
st.success(summary)

# Inventory Monitoring Section
st.header("Inventory Monitoring")
low_inventory = identify_low_inventory("inventory_monitoring.csv")
inventory_df = pd.DataFrame(low_inventory)

# Safely convert relevant columns to numeric (coerce errors to NaN)
numeric_cols = ["Inventory", "Stock Levels"]
for col in numeric_cols:
    if col in inventory_df.columns:
        inventory_df[col] = pd.to_numeric(inventory_df[col], errors='coerce')

st.write("Low Inventory Products:")
st.dataframe(inventory_df)

# Pricing Optimization Section
st.header("Pricing Optimization")
pricing_df, pricing_summary = optimize_pricing()
pricing_df['Price'] = pd.to_numeric(pricing_df['Price'], errors='coerce')
pricing_df['Adjusted Price'] = pd.to_numeric(pricing_df['Adjusted Price'], errors='coerce')

st.write("Optimized Prices:")
st.dataframe(pricing_df)
st.write("Mistral Insight:")
st.success(pricing_summary)

# Multi-Agent Collaboration
st.header("Multi-Agent Collaboration")
agent_df = run_multiagent_simulation()

# Ensure numeric conversion doesn't crash Streamlit
numeric_cols_agent = ["Store ID", "Product ID", "Customer Demand Trend"]
for col in numeric_cols_agent:
    if col in agent_df.columns:
        agent_df[col] = pd.to_numeric(agent_df[col], errors='coerce')

st.write("Agent Collaboration Results:")
st.dataframe(agent_df)

# Mistral Insight via Ollama
st.header("Ask Mistral Anything")
query_text = st.text_area("Ask Mistral about your inventory strategy:")
if st.button("Get Insight"):
    with st.spinner("Querying Mistral..."):
        response = get_mistral_insight(query_text)
        st.subheader("Mistral Response:")
        st.write(response)
