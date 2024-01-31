import requests
from bs4 import BeautifulSoup
##################fetching data from Gfinance

def get_stock_dataN(symbol):
    url = f"https://www.google.com/finance/quote/{symbol}:INDEXNSE"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    stock_name = soup.find('div', class_='zzDege').text
    stock_price = soup.find('div', class_='YMlKec fxKbKc').text
    #proloss = soup.find('div', class_='P2Luy Ebnabc ZYVHBb').text
    #stock_profit = soup.find('div', class_='').text
    
    return [stock_name,stock_price,symbol]
  
def get_stock_dataNB(symbol):
    url = f"https://www.google.com/finance/quote/{symbol}:NSE"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
 
    stock_name = soup.find('div', class_='zzDege').text
    stock_price = soup.find('div', class_='YMlKec fxKbKc').text
    #proloss = soup.find('div', class_='P2Luy Ebnabc ZYVHBb').text
    #stock_profit = soup.find('div', class_='').text
    
    return [stock_name,stock_price,symbol]

def get_stock_dataB(symbol):
    url = f"https://www.google.com/finance/quote/{symbol}:INDEXBOM"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
 
    stock_name = soup.find('div', class_='zzDege').text
    stock_price = soup.find('div', class_='YMlKec fxKbKc').text
    #proloss = soup.find('div', class_='P2Luy Ebnabc ZYVHBb').text
    #stock_profit = soup.find('div', class_='JwB6zf').text
    #print(f"{stock_name} ({symbol}): {stock_price}")    
    return [stock_name,stock_price,symbol]
 

nifty = get_stock_dataN('NIFTY_50')
sensex =  get_stock_dataB('SENSEX')
sbi = get_stock_dataN('NIFTY_BANK')
hdfc = get_stock_dataN('NIFTY_IT')

print(nifty)import yfinance as yf
import plotly.graph_objects as go
import pandas_ta as ta
from plotly.subplots import make_subplots

# Function to fetch stock data
def fetch_stock_data(symbol, st, en):
    try:
        # Fetch historical stock data
        stock_data = yf.download(symbol, start=st, end=en)
        return stock_data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

# Function to calculate RSI
def calculate_rsi(stock_data):
    stock_data['rsi'] = ta.rsi(stock_data['Close'], length=14)
    return stock_data['rsi']

# Function to calculate Bollinger Bands
def calculate_bollinger(stock_data):
    bbands = ta.bbands(stock_data['Close'], length=20, std=2)
    return bbands.iloc[:, 1]  # Return the middle band

# Function to calculate VWAP
def calculate_vwap(stock_data):
    stock_data['typical_price'] = (stock_data['High'] + stock_data['Low'] + stock_data['Close']) / 3
    stock_data['vwap'] = ta.sma(stock_data['typical_price'] * stock_data['Volume'], length=14) / ta.sma(stock_data['Volume'], length=14)
    return stock_data['vwap']

# Function to calculate P/E ratio
def calculate_pe_ratio(stock_data):
    # Example: Assuming the P/E ratio is calculated using Close and Earnings per Share (EPS)
    stock_data['pe_ratio'] = stock_data['Close'] / 10  # Replace this with your actual calculation
    return stock_data['pe_ratio']

# Function to calculate EBITDA
def calculate_ebitda(stock_data):
    # Example: Assuming EBITDA is calculated as Revenue minus Operating Expenses
    stock_data['ebitda'] = stock_data['Close'] * 0.8  # Replace this with your actual calculation
    return stock_data['ebitda']

# Function to calculate CAPEX
def calculate_capex(stock_data):
    # Example: Assuming CAPEX is calculated based on Capital Expenditure
    stock_data['capex'] = stock_data['Close'] * 0.05  # Replace this with your actual calculation
    return stock_data['capex']

# Function to plot stock data with selected filters
def plot_stock_filters(symbol, stock_data, selected_filters):
    if stock_data is not None and not stock_data.empty:
        # Create subplots
        fig = make_subplots(rows=len(selected_filters), cols=1, shared_xaxes=True, subplot_titles=selected_filters)

        for i, filter_option in enumerate(selected_filters):
            # Filter the data based on the selected option
            if filter_option == 'RSI':
                filtered_data = calculate_rsi(stock_data)
            elif filter_option == 'Bollinger':
                filtered_data = calculate_bollinger(stock_data)
            elif filter_option == 'VWAP':
                filtered_data = calculate_vwap(stock_data)
            elif filter_option == 'High':
                filtered_data = stock_data['High']
            elif filter_option == 'Low':
                filtered_data = stock_data['Low']
            elif filter_option == 'Close':
                filtered_data = stock_data['Close']
            elif filter_option == 'Open':
                filtered_data = stock_data['Open']
            elif filter_option == 'P/E ratio':
                filtered_data = calculate_pe_ratio(stock_data)
            elif filter_option == 'EBITDA':
                filtered_data = calculate_ebitda(stock_data)
            elif filter_option == 'CAPEX':
                filtered_data = calculate_capex(stock_data)
            else:
                print(f"Invalid filter option: {filter_option}. Skipping.")
                continue

            # Add trace to subplot
            fig.add_trace(go.Scatter(x=stock_data.index, y=filtered_data, mode='lines', name=filter_option), row=i+1, col=1)

        # Update layout
        fig.update_layout(title=f"{symbol} Stock Price with Selected Filters",
                          xaxis_title="Date",
                          template="plotly_dark",
                          showlegend=True,
                          height=len(selected_filters) * 300)  # Adjust the height based on the number of filters

        # Show the plot
        fig.show()

    else:
        print("No data available for the given stock symbol.")

# Example: User input for stock symbol and selected filters
user_stock_symbol = input("Enter stock symbol: ") + ".NS"
user_selected_filters = input("Enter selected filters (comma-separated, e.g., RSI, Bollinger, VWAP, High, Low, Close, Open, EBITDA, CAPEX): ").split(',')
stdate = input("start date: ")
enddate = input("end date: ")
# Fetch and plot stock data with selected filters
stock_data = fetch_stock_data(user_stock_symbol,stdate,enddate)
plot_stock_filters(user_stock_symbol, stock_data, user_selected_filters)
