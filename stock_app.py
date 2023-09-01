import streamlit as st
import yfinance as yf
import pandas as pd
import io

def fetch_stock_data(ticker_symbol, start_date=None):
    stock_data = yf.download(ticker_symbol, start=start_date)
    return stock_data

def fetch_recent_shares_outstanding(ticker_symbol):
    ticker_obj = yf.Ticker(ticker_symbol)
    shares_outstanding = ticker_obj.info['sharesOutstanding']
    return shares_outstanding

# Sample list of Japanese stocks
stocks = [
    ("Toyota", "7203.T"),
    ("Sony", "6758.T"),
    ("Honda", "7267.T"),
    ("Nintendo", "7974.T"),
    ("Bandai Namco", "7832.T"),
    ("Square Enix", "9684.T"),
    ("Capcom", "9697.T"),
    ("Konami", "9766.T"),
    ("Sega", "6460.T"),
    ("Koei Tecmo", "3635.T")
]

stock_name_to_symbol = {name: symbol for name, symbol in stocks}

st.title("Japanese Stock Data Fetcher")
st.subheader("by tkdeniz")

selected_stock = st.selectbox("Select a stock:", [name for name, _ in stocks])
start_date = st.date_input("Select a start date:")

if st.button("Fetch Data"):
    ticker = stock_name_to_symbol[selected_stock]
    data = fetch_stock_data(ticker, start_date)
    
    # Approximate daily market cap
    shares_outstanding = fetch_recent_shares_outstanding(ticker)
    data['Market Cap'] = data['Close'] * shares_outstanding
    st.write(data)

    # Convert DataFrame to Excel and create download link
    excel_bytes = io.BytesIO()
    data.to_excel(excel_bytes, index=True, engine='openpyxl')
    excel_bytes.seek(0)
    st.download_button(
        label="Download Excel",
        data=excel_bytes,
        file_name=f"{selected_stock}_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
