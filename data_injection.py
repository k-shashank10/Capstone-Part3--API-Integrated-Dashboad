import pandas as pd
import requests
import os

def load_data():
    """Loads and merges route operations and trade route metadata, plus geopolitical events."""
    if os.path.exists('weekly_route_operations.csv') and os.path.exists('trade_routes.csv'):
        ops_df = pd.read_csv('weekly_route_operations.csv')
        routes_df = pd.read_csv('trade_routes.csv')
        
        # Merge operation data with trade route details (including country info)
        df = pd.merge(ops_df, routes_df, on='route_id', how='inner')
        df['date'] = pd.to_datetime(df['date'])
        df['Year'] = df['date'].dt.year
    else:
        df = pd.DataFrame()

    if os.path.exists('geopolitical_events.csv'):
        geo_df = pd.read_csv('geopolitical_events.csv')
    else:
        geo_df = pd.DataFrame()

    return df, geo_df

def fetch_live_api(base_currency):
    """Simple GET request to fetch live foreign exchange conversion rates."""
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("rates", {})
    except Exception:
        pass
    return None