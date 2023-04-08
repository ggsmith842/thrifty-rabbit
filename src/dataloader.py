import sqlite3
import pandas as pd 
import alphavantage as av
import time

def data_loader():
    #Build portfolio
    portfolio = [
        "SPY",
        "WMT",
        "JNPR",
        "CVS",
        "BAC",
        "JNJ",
        "ABB",
        "ORCL",
    ] 

    prices = pd.DataFrame()
    for symbol in portfolio:
        df = av.get_monthly_adj_ts(symbol=symbol)
        df["symbol"] = symbol
        prices = pd.concat([prices,df])
        time.sleep(10) #sleep to avoid going over 5 calls per minute limit
    prices.sort_values('DATE')

    # Create sqlite database connection object
    conn = sqlite3.connect('sqlite3.db')

    # Write dataframe to a table in sqlite database
    prices.to_sql('Prices', conn, if_exists='append', index=False)

    # Close connection object
    conn.close()
    return 

if __name__ == "__main__":
    data_loader()
