Video explaining the project:- https://youtu.be/0L45oqQysd8?si=2TJt1r6HYu1ezm1E
# Smart Inventory Monitoring System

A multi-agent AI system for retail inventory management that combines demand forecasting, inventory monitoring, pricing optimization, and LLM-based decision support.

The system uses time-series forecasting and rule-based inventory logic to analyze retail data, while multiple software agents coordinate store, warehouse, supplier, and customer demand information. Mistral through Ollama is used to generate additional insights for inventory and pricing decisions.

## Features

* Demand forecasting for upcoming sales
* Low-stock inventory detection
* Rule-based pricing optimization
* Multi-agent inventory collaboration
* Store, warehouse, supplier, and customer agents
* Mistral-powered inventory insights
* Interactive Streamlit dashboard
* CSV-based data processing and output
* Real-time Mistral queries through Ollama

## System Architecture

```text
                    Retail Data
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
   Demand Data    Inventory Data   Pricing Data
          │             │             │
          ▼             ▼             ▼
      Demand       Inventory       Pricing
    Forecasting    Monitoring     Optimization
          │             │             │
          └─────────────┼─────────────┘
                        │
                        ▼
                Multi-Agent System
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
   Store Agent     Warehouse Agent   Supplier Agent
       │                │                │
       └────────────────┼────────────────┘
                        │
                 Customer Agent
                        │
                        ▼
                Mistral via Ollama
                        │
                        ▼
              Inventory Insights
                        │
                        ▼
              Streamlit Dashboard
```

## Technology Stack

| Component          | Technology                         |
| ------------------ | ---------------------------------- |
| Language           | Python                             |
| Dashboard          | Streamlit                          |
| Data Processing    | Pandas                             |
| Demand Forecasting | Statsmodels                        |
| Forecasting Model  | Holt-Winters Exponential Smoothing |
| LLM                | Mistral                            |
| LLM Runtime        | Ollama                             |
| API Communication  | Requests                           |
| Data Storage       | CSV                                |

## Demand Forecasting

The demand forecasting module uses the Holt-Winters Exponential Smoothing model from `statsmodels`.

The input sales data is processed chronologically and duplicate dates are removed before forecasting.

The model uses:

```text
Trend: Additive
Seasonality: Additive
Seasonal Period: 7 days
Forecast Horizon: 5 days
```

The forecasted sales values are then passed to Mistral through Ollama to generate a short interpretation of the expected demand trend.

```text
Historical Sales Data
        │
        ▼
Data Cleaning
        │
        ▼
Holt-Winters Model
        │
        ▼
5-Day Demand Forecast
        │
        ▼
Mistral Trend Analysis
```

## Inventory Monitoring

The inventory monitoring module identifies products with stock levels below a predefined threshold.

The current implementation uses:

```text
Stock Level < 10
```

as the low-inventory condition.

The system filters inventory data by store and returns products that require attention.

## Pricing Optimization

The pricing module applies a rule-based pricing strategy using sales volume and current price.

A product is considered for a price adjustment when:

```text
Sales Volume < Average Sales Volume
AND
Price > Average Price
```

For products satisfying both conditions, the current price is reduced by 5%.

```text
Adjusted Price = Price × 0.95
```

Mistral is then used to explain the resulting pricing strategy based on the processed data.

## Multi-Agent System

The project uses separate software agents for different parts of the inventory workflow.

### Store Agent

The Store Agent monitors stock levels for a specific store.

Responsibilities:

* Check current inventory
* Identify low-stock products
* Generate restock requests

### Warehouse Agent

The Warehouse Agent checks whether the requested quantity is available in the warehouse.

It returns either:

```text
Request fulfilled
```

or:

```text
Insufficient stock
```

### Supplier Agent

If the warehouse does not have enough stock, the Supplier Agent generates a supplier order using the product's supplier lead time.

Example:

```text
Order placed for 20 units.
Estimated delivery in 5 days.
```

### Customer Agent

The Customer Agent analyzes historical sales data to calculate demand trends.

For products with sufficient historical data, it uses a 7-day rolling average of sales quantity.

## Agent Collaboration Workflow

```text
Store Agent
    │
    │ Low Stock Detected
    ▼
Restock Request
    │
    ▼
Warehouse Agent
    │
    ├── Stock Available
    │       │
    │       ▼
    │   Fulfill Request
    │
    └── Insufficient Stock
            │
            ▼
       Supplier Agent
            │
            ▼
       Supplier Order

Customer Agent
      │
      ▼
Demand Trend
      │
      └──────────────┐
                     ▼
               Mistral Agent
                     │
                     ▼
             Inventory Insight
```

For each low-stock product, the system combines warehouse availability, supplier information, and customer demand trends before sending the information to Mistral for an inventory recommendation.

## Mistral Integration

Mistral is accessed locally through the Ollama API.

The application communicates with:

```text
http://localhost:11434/api/generate
```

The default model is:

```text
mistral
```

The integration supports two main use cases:

1. Generating insights from demand forecasts and pricing data.
2. Generating inventory decisions using multi-agent information.

Users can also enter custom questions through the Streamlit dashboard and send them directly to Mistral.

## Streamlit Dashboard

The application provides a single dashboard containing:

* Demand Forecasting
* Inventory Monitoring
* Pricing Optimization
* Multi-Agent Collaboration
* Mistral Insights
* Custom Mistral Query Interface

The dashboard displays processed data using Streamlit dataframes and provides generated Mistral insights alongside the analytical results.

## Input Data

The project uses three CSV datasets.

### demand_forecasting.csv

Contains historical sales information used for demand forecasting.

Relevant fields include:

```text
Date
Product ID
Sales Quantity
```

### inventory_monitoring.csv

Contains inventory and supplier information.

Relevant fields include:

```text
Store ID
Product ID
Stock Levels
Supplier Lead Time (days)
```

### pricing_optimization.csv

Contains product pricing and sales information.

Relevant fields include:

```text
Product ID
Store ID
Price
Sales Volume
```

## Output

The multi-agent simulation generates:

```text
agent_collaboration_output.csv
```

The output contains information such as:

```text
Product ID
Store ID
Restock Request
Warehouse Response
Supplier Response
Customer Demand Trend
Mistral Insight
```

## Project Structure

```text
smart-inventory-monitoring/
│
├── app.py
├── main.py
│
├── agent_collaboration.py
├── demand_forecasting.py
├── inventory_monitoring.py
├── pricing_optimization.py
├── ollama_interface.py
│
├── demand_forecasting.csv
├── inventory_monitoring.csv
├── pricing_optimization.csv
├── agent_collaboration_output.csv
│
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/smart-inventory-monitoring.git
cd smart-inventory-monitoring
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Ollama Setup

Install Ollama and make sure it is running locally.

Pull the Mistral model:

```bash
ollama pull mistral
```

Verify that the model is available:

```bash
ollama list
```

The application expects Ollama to be accessible at:

```text
http://localhost:11434
```

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## Running the Multi-Agent Simulation

The multi-agent workflow can also be executed independently through the Python module.

The simulation:

1. Loads inventory, pricing, and demand data.
2. Creates the Store, Warehouse, Supplier, and Customer agents.
3. Identifies low-stock products.
4. Generates restock requests.
5. Checks warehouse availability.
6. Places supplier orders when required.
7. Calculates customer demand trends.
8. Sends the combined information to Mistral.
9. Saves the results to `agent_collaboration_output.csv`.

## Requirements

The main Python dependencies are:

```text
streamlit
pandas
statsmodels
requests
```

Ollama and the Mistral model are required separately for LLM-based functionality.

## Limitations

The current system uses rule-based logic for inventory thresholds and pricing adjustments. The demand forecasting component is based on historical sales data and Holt-Winters exponential smoothing.

The multi-agent system represents software agents that coordinate through Python functions and data structures. It does not use a dedicated multi-agent framework.

Mistral insights depend on the locally running Ollama model and the quality of the information provided in each prompt.

## Future Improvements

* Add automated inventory replenishment
* Support multiple warehouses and stores
* Add more advanced demand forecasting models
* Include external market and competitor pricing data
* Add persistent database storage
* Add authentication and user roles
* Deploy the application to the cloud
* Add more specialized agents
* Add historical dashboards and inventory analytics

## Author

**Tejvir Singh Grewal**

B.Tech Computer Science Engineering,
Thapar Institute of Engineering & Technology

