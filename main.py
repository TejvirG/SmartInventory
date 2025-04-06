from demand_forecasting import forecast_demand
from inventory_monitoring import identify_low_inventory
from pricing_optimization import optimize_pricing
from agent_collaboration import run_multiagent_simulation

# Demand Forecasting
forecast, insight1 = forecast_demand()
print("Forecasted Demand:\n", forecast)
print("Mistral Insight:", insight1)

# Inventory Monitoring
df_inventory = identify_low_inventory()
print("\nLow Inventory:\n", df_inventory)

# Pricing Optimization
df_pricing, insight2 = optimize_pricing()
print("\nOptimized Prices:\n", df_pricing)
print("Mistral Insight:", insight2)

# Multi-agent Simulation
agent_output = run_multiagent_simulation()
print("\nAgent Simulation Output:\n", agent_output)
