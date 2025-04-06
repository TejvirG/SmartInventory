import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from ollama_interface import get_mistral_insight

def forecast_demand(file_path="demand_forecasting.csv"):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').drop_duplicates(subset='Date')
    df.set_index('Date', inplace=True)
    df['Sales Quantity'] = df['Sales Quantity'].fillna(method='ffill')

    model = ExponentialSmoothing(df['Sales Quantity'], trend='add', seasonal='add', seasonal_periods=7)
    model_fit = model.fit()
    forecast = model_fit.forecast(5)

    forecast_list = forecast.tolist()
    
    summary_prompt = f"The forecasted sales for the next 5 days are {forecast_list}. Summarize the trend."
    insight = get_mistral_insight(summary_prompt)

    return forecast_list, insight
