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

print(nifty)