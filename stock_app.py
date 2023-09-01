import streamlit as st
import yfinance as yf

def fetch_stock_data(ticker_symbol, start_date=None):
    stock_data = yf.download(ticker_symbol, start=start_date)
    return stock_data

# Sample list of Japanese stocks
stocks = [
    ("Toyota", "7203.T"),
    ("Sony", "6758.T"),
    ("Honda", "7267.T"),
    ("Bandai Namco", "7832.T"),
    ("Square Enix", "9684.T"),
    ("Capcom", "9697.T"),
    ("Konami", "9766.T"),
    ("Sega", "6460.T"),
    ("Koei Tecmo", "3635.T")
]

stock_name_to_symbol = {name: symbol for name, symbol in stocks}

st.title("Japanese Stock Data Fetcher")

selected_stock = st.selectbox("Select a stock:", [name for name, _ in stocks])
start_date = st.date_input("Select a start date:")

if st.button("Fetch Data"):
    ticker = stock_name_to_symbol[selected_stock]
    data = fetch_stock_data(ticker, start_date)
    st.write(data)
