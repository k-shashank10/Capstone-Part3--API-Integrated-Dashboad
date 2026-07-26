# Part 3: API-Integrated Supply Chain Intelligence Dashboard

## Project Overview & Task Description
This repository represents **Part 3** of the End-to-End Applied AI & ML Data Product Capstone Project. The objective of this stage is to turn a cleaned analytics asset into a live, interactive, public-facing web dashboard that enables non-technical stakeholders to explore operational metrics, examine trends, and analyze supply chain resilience.

In compliance with the project guidelines, this application is fully self-contained, runs top-to-bottom from a clean environment using `requirements.txt`, and features:
* **Interactive Input Widgets:** Filter controls using `st.selectbox` and `st.slider` to dynamically alter the view state.
* **Distinct Visualizations:** Three separate Plotly charts updating in real-time based on user selections with custom axis labels and tooltips.
* **Live Filtered Data Tables:** Interactive `st.dataframe` views showing row-level operational records, geopolitical disruption logs, and a CSV data download button.
* **Live External REST API Integration:** A live connection using Python's `requests` library to fetch and parse external currency exchange data on the fly, dynamically converting freight costs.

* **Live App URL:** [https://capstone-part3--api-integrated-dashboad-5cgtqcrzrgnytsgiqnxngd.streamlit.app/](https://capstone-part3--api-integrated-dashboad-5cgtqcrzrgnytsgiqnxngd.streamlit.app/)

---

##  Project Structure

```text
Part 3/
│
├── app.py                      # Main Streamlit user interface and dashboard layout
├── data_injection.py           # Backend module for loading, merging CSV data & live API calls
├── requirements.txt            # Project dependencies
├── trade_routes.csv            # International trade route characteristics
├── geopolitical_events.csv     # Simulated geopolitical disruptions, severity scales, and crisis logs
└── weekly_route_operations.csv # Weekly trade route operations, delays, costs, and risk metrics
```
---
## 1. Dataset Context & Scope
This dataset simulates global supply chain operations and trade disruptions across major international trade routes from 2015 to 2026. It combines logistics, commodity markets, geopolitical events, and transportation risk factors to create a realistic environment for data analysis and operational monitoring.

### **Included Data Files**
* `trade_routes.csv` – International trade route characteristics.
* `geopolitical_events.csv` – Simulated geopolitical disruptions, severity scales, and crisis logs.
* `weekly_route_operations.csv` – Weekly trade route operations, delays, costs, and risk metrics.

### **Key Features Tracked**
* Global trade routes and logistics networks
* Shipping delays and freight costs
* Port congestion and container availability
* Commodity market indicators
* Weather disruption scores
* Geopolitical risk scores and crisis logs
* Carbon emissions estimates
* Route status classification
* Trade volume analysis

### **Major Historical & Simulated Events**
* COVID-19 Supply Chain Shock (2020)
* Russia–Ukraine Conflict (2022)
* Red Sea Shipping Crisis (2024)
* Strait of Hormuz Disruption Scenario (2026)

---

## 2. External REST API Integration
To satisfy the live API integration requirement, this dashboard connects to a public REST endpoint using Python's requests library:
* **API Used:** ExchangeRate-API (https://open.er-api.com).
* **Purpose:** FFetches real-time foreign exchange conversion rates to evaluate live cost adjustments and dynamically convert freight costs across multiple base currencies (USD, EUR, GBP, INR, AUD, CAD, JPY).

---

## 3. Setup & Execution Instructions

To run this dashboard locally from a clean environment, follow these steps:

###  Prerequisites
* Ensure **Python 3.8+** is installed on your local machine.

###  Repository Setup
Clone the repository and ensure all required CSV data files (`weekly_route_operations.csv`, `trade_routes.csv`, and `geopolitical_events.csv`) are placed together in the project root directory alongside `app.py` and `data_injection.py`.

###  Install Dependencies
Open your terminal or PowerShell in the project directory and install the required Python packages:
```bash
pip install -r requirements.txt
```
### Launch The Dash board
Launch the interactive web interface using Streamlit:
```bash
streamlit run app.py
```
Open the local browser link provided in your terminal (typically `http://localhost:8501`)

---
## 4. References & Data Sources

### Official Documentation & Libraries
* **Streamlit Documentation:** For interactive dashboard layout, session state, and widget management. Available at: [https://docs.streamlit.io/](https://docs.streamlit.io/)
* **Plotly Python Graphing Library:** For responsive, interactive operational charts and data visualization. Available at: [https://plotly.com/python/](https://plotly.com/python/)
* **Requests HTTP Library:** For connecting to external currency exchange APIs. Available at: [https://requests.readthedocs.io/](https://requests.readthedocs.io/)

### Academic Class Notes & Faculty Materials
* **Class Lectures & Presentations:** Core theoretical frameworks on data product design, dashboard modularity, and real-time state management provided by faculty during lecture sessions.
* **Faculty Code & Lab Boilerplates:** Reference scripts, structural patterns, and API integration templates shared during practical lab hours.
* **MSSAI Curriculum Guidelines:** Applied data product scoping, UI/UX structuring standards, and deployment best practices outlined in the MSSAI curriculum framework.

### Data Sources & External APIs
* **Global Supply Chain Disruption Dataset (2015–2026):** Created and published by Kuldeep Jangra on Kaggle. Available via Kaggle
* **ExchangeRate-API:** Public live REST endpoint for real-time currency conversion (`https://open.er-api.com`)
