import streamlit as st
import yfinance as yf
import pandas as pd
import io

from openpyxl.utils.dataframe import dataframe_to_rows

def auto_size_columns(ws):
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

def fetch_stock_data(ticker_symbol, start_date=None):
    stock_data = yf.download(ticker_symbol, start=start_date)
    return stock_data[['Close']]  # Only fetch the 'Close' column

def fetch_recent_shares_outstanding(ticker_symbol):
    ticker_obj = yf.Ticker(ticker_symbol)
    return ticker_obj.info.get('sharesOutstanding', None)  # Use .get() method with a default value

def fetch_all_data(stocks, start_date):
    with pd.ExcelWriter('stock_data.xlsx', engine='openpyxl') as writer:
        for stock_name, ticker_symbol in stocks:
            data = fetch_stock_data(ticker_symbol, start_date)
            market_cap = fetch_recent_market_cap(ticker_symbol)
            if market_cap is not None:
                data['Market Cap'] = market_cap
            data.to_excel(writer, sheet_name=stock_name)
            
            # Auto-size columns for the current sheet
            ws = writer.sheets[stock_name]
            auto_size_columns(ws)
        
        # Ensure the first sheet is visible
        first_sheet_name = stocks[0][0]
        writer.sheets[first_sheet_name].sheet_state = 'visible'
    return 'stock_data.xlsx'

# List of Japanese and Korean gaming companies
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
    ("Koei Tecmo", "3635.T"),
    ("Nexon", "3659.T"),
    ("Netmarble", "251270.KS"),
    ("NCSoft", "036570.KS"),
    ("Kakao Games", "293490.KS"),
    ("CyberAgent", "4751.T"),
    ("GungHo Online", "3765.T"),
    ("Dena", "2432.T"),
    ("Mixi", "2121.T"),
    ("Pearl Abyss", "263750.KS"),
    ("Com2uS", "078340.KS"),
    ("Webzen", "069080.KS"),
    ("Smilegate", "141080.KS")
]

stock_name_to_symbol = {name: symbol for name, symbol in stocks}

st.title("Japanese & Korean Gaming Stock Data Fetcher")
st.subheader("by tkdeniz")

selected_stock = st.selectbox("Select a stock:", [name for name, _ in stocks])
start_date = st.date_input("Select a start date:")

if st.button("Fetch Data"):
    # Display a loading message
    loading_message = st.empty()
    loading_message.text('Fetching data... Please wait.')
    
    file_path = fetch_all_data(stocks, start_date)

    # Clear the loading message or replace with another message
    loading_message.text('Data fetched successfully!')
    
    with open(file_path, 'rb') as f:
        excel_bytes = f.read()
    
    st.download_button(
        label="Download Excel",
        data=excel_bytes,
        file_name="all_stock_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
