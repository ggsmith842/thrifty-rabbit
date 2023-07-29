"""
Utility module to load data into a sqlite3 database.

This module provides a function to load pricing data into a sqlite3 database.

The function takes a portfolio of ticker symbols as input and a period of time as input.
The function then downloads the pricing data for the portfolio from 
Yahoo Finance and loads it into a sqlite3 database.

The module also provides a main function that can be used to test the function.

"""

#!/usr/bin/env python #
import sqlite3
import yfinance as yf


def data_loader(portfolio, period="5y", tosqlite=False):
    """
    Helper function to load pricing data into
    a sqllite3 database.

    Args:
        portfolio (list): A list of ticker symbols.
        period (str, optional): The period of time for the pricing data. Defaults to "10y". 
        period values: “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
        tosqlite (bool, optional): Load the data into a sqlite3 database. Defaults to False.

    Returns:
        DataFrame: The pricing data for the portfolio only if tosqlite is False.
    """

    data = yf.download(portfolio, group_by="Ticker", period=period)
    data = data.iloc[:, data.columns.get_level_values(1) == "Close"]
    data = data.dropna()
    data.columns = data.columns.droplevel(1)

    if tosqlite:
        # Create sqlite database connection object
        try:
            conn = sqlite3.connect("advisor_db.db")
        except sqlite3.OperationalError:
            conn = sqlite3.connect("advisor_db.db")
            conn.execute("CREATE TABLE prices (date DATE, ticker TEXT, close FLOAT)")

        # Write dataframe to a table in sqlite database
        data.to_sql("prices", conn, if_exists="replace", index=False)

        # Close connection object
        conn.close()
    else:
        return data.reset_index()


if __name__ == "__main__":
    portfolio_string = ["SPY WMT JNPR CVS BAC JNJ ABBNY SHEL ORCL USRT"]
    data_loader(portfolio=portfolio_string)
