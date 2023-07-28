"""
Utility module to load data into a sqlite3 database
"""
import sqlite3
import yfinance as yf


def data_loader(portfolio, period="10yr"):
    """
    Helper function to load pricing data into
    a sqllite3 database.
    """

    data = yf.download(portfolio, group_by="Ticker", period=period)
    data = data.iloc[:, data.columns.get_level_values(1) == "Close"]
    data = data.dropna()
    data.columns = data.columns.droplevel(1)

    # Create sqlite database connection object
    conn = sqlite3.connect("sqlite3.db")

    # Write dataframe to a table in sqlite database
    data.to_sql("Prices", conn, if_exists="append", index=False)

    # Close connection object
    conn.close()
    return


if __name__ == "__main__":
    portfolio = ["SPY WMT JNPR CVS BAC JNJ ABBNY SHEL ORCL"]

    data_loader(portfolio=portfolio)
