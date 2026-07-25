import streamlit as st
import pandas as pd
import plotly.express as px
from data_injection import load_data, fetch_live_api

# --- PAGE SETUP ---
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

st.title("Global Supply Chain & Trade Disruption Dashboard")
st.write("Welcome! Explore global trade corridors, logistics performance metrics, geopolitical risk factors, and real-time currency conversions.")

# --- LOAD DATA ---
df, geo_df = load_data()

# --- SIDEBAR: LIVE API INTEGRATION & CURRENCY CONVERSION ---
st.sidebar.header("🌐 Live External API")
currencies = ["USD", "EUR", "GBP", "INR", "AUD", "CAD", "JPY"]
base_curr = st.sidebar.selectbox("Select Base Currency", currencies)

# Fetch live rates based on selected base currency using GET request
rates = fetch_live_api(base_curr)

if rates:
    st.sidebar.success("API Connected Successfully!")
    st.sidebar.subheader("Conversion Rates:")
    target_currencies = [c for c in currencies if c != base_curr]
    for target in target_currencies[:4]:
        rate_val = rates.get(target, 1.0)
        st.sidebar.write(f"1 {base_curr} = {rate_val:.4f} {target}")
else:
    st.sidebar.warning("Could not fetch live API data.")

st.sidebar.markdown("---")

# --- SIDEBAR FILTER WIDGETS ---
st.sidebar.header("Filter Controls")

if not df.empty:
    years = sorted(df['Year'].unique())
    selected_year = st.sidebar.selectbox("Select Year", years)

    methods = ["All"] + list(df['shipping_method'].unique())
    selected_method = st.sidebar.selectbox("Select Shipping Method", methods)

    max_delay = st.sidebar.slider("Max Shipping Delay (Days)", 0, int(df['shipping_delay_days'].max()), int(df['shipping_delay_days'].max()))

    filtered_df = df[df['Year'] == selected_year]
    if selected_method != "All":
        filtered_df = filtered_df[filtered_df['shipping_method'] == selected_method]
    filtered_df = filtered_df[filtered_df['shipping_delay_days'] <= max_delay]
else:
    filtered_df = pd.DataFrame()
    st.error("Dataset files not found in the folder.")

# --- CURRENCY MULTIPLIER LOGIC ---
usd_rates = fetch_live_api("USD")
conversion_multiplier = 1.0
if usd_rates and base_curr in usd_rates:
    conversion_multiplier = usd_rates[base_curr]

display_df = filtered_df.copy()
if not display_df.empty:
    display_df['freight_cost_converted'] = display_df['freight_cost_usd'] * conversion_multiplier

# --- KEY METRICS DISPLAY ---
if not display_df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Routes Analyzed", len(display_df))
    col2.metric(f"Average Freight Cost ({base_curr})", f"{base_curr} {display_df['freight_cost_converted'].mean():,.2f}")
    col3.metric("Average Delay (Days)", f"{display_df['shipping_delay_days'].mean():.1f}")

    st.markdown("---")

    # --- PLOTLY CHARTS (With clear axis labels & tooltips) ---
    st.subheader("Visual Analysis")
    
    col_a, col_b = st.columns(2)

    with col_a:
        cost_df = display_df.groupby('shipping_method')['freight_cost_converted'].mean().reset_index()
        fig1 = px.bar(
            cost_df, 
            x='shipping_method', 
            y='freight_cost_converted', 
            title=f"Average Freight Cost by Method ({base_curr})",
            labels={'shipping_method': 'Shipping Method', 'freight_cost_converted': f'Avg Freight Cost ({base_curr})'}
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        fig2 = px.scatter(
            display_df, 
            x='geopolitical_risk_score', 
            y='shipping_delay_days', 
            color='route_status', 
            title="Delay vs Geopolitical Risk",
            labels={'geopolitical_risk_score': 'Geopolitical Risk Score', 'shipping_delay_days': 'Shipping Delay (Days)'}
        )
        st.plotly_chart(fig2, use_container_width=True)

    # --- COUNTRY TO COUNTRY TRADE CORRIDORS ---
    st.subheader("Country-to-Country Trade Corridors")
    country_trade = display_df.groupby(['origin_country', 'destination_country'])['trade_volume_tonnes'].sum().reset_index()
    fig_country = px.bar(
        country_trade, 
        x='origin_country', 
        y='trade_volume_tonnes', 
        color='destination_country',
        title="Total Trade Volume (Tonnes) by Origin and Destination Country",
        labels={'origin_country': 'Origin Country', 'trade_volume_tonnes': 'Total Trade Volume (Tonnes)', 'destination_country': 'Destination Country'}
    )
    st.plotly_chart(fig_country, use_container_width=True)

    # --- DATA TABLE & EXPORT BUTTON ---
    st.subheader("Filtered Route Data Table")
    st.dataframe(display_df)

    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_supply_chain_data.csv",
        mime="text/csv"
    )

# --- GEOPOLITICAL EVENTS SECTION ---
st.markdown("---")
st.subheader("Geopolitical Disruptions Log")

if not geo_df.empty:
    st.dataframe(geo_df)
else:
    st.write("Geopolitical events data not available.")