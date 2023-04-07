import requests
import os
import pandas as pd


def get_monthly_adj_ts(symbol):
    '''
    given a ticker symbol, return a time series as a pandas dataframe
    '''    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={os.getenv('APIKEY')}"
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data["Monthly Adjusted Time Series"]).T.reset_index()
    

    df = df.rename(columns={"index": "DATE",
                "1. open": "OPEN",
                "2. high": "HIGH",
                "3. low": "LOW",
                "4. close": "CLOSE",
                "5. adjusted close": "ADJ_CLOSE",
                "6. volume": "VOLUME",
                "7. dividend amount": "YIELD"
             }
    )

    
    df['DATE'] = pd.to_datetime(df['DATE'])
    df[['OPEN', 'HIGH', 'LOW', 'CLOSE', 'ADJ_CLOSE', 'VOLUME', 'YIELD']] = df[['OPEN', 'HIGH', 'LOW', 'CLOSE', 'ADJ_CLOSE', 'VOLUME', 'YIELD']].apply(pd.to_numeric)

    return df


def get_fundamentals(symbol):
    '''
    given a ticker symbol, return a time series as a pandas dataframe
    '''    
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={os.getenv('APIKEY')}"
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data["Monthly Adjusted Time Series"]).T

    return df