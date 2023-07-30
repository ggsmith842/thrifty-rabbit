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


def data_loader(portfolio, period="5y", tosqlite=False, database_name="sqlite.db"):
    """
    Helper function to load pricing data into
    a sqllite3 database.

    Args:
        portfolio (list): A list of ticker symbols.
        period (str, optional): The period of time for the pricing data. Defaults to "10y".
        period values: “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
        tosqlite (bool, optional): Load the data into a sqlite3 database. Defaults to False.
        database_name (string, optional): If tosqlite True, provide a name with .db at the end.

    Returns:
        DataFrame: The pricing data for the portfolio only if tosqlite is False.
    """

    closing_prices = yf.download(tickers=portfolio, period=period)["Close"]
    data = (
        closing_prices
        .reset_index()
        .melt(id_vars=["Date"], var_name="Symbol")
        .rename(columns={"Date": "date", "Symbol": "symbol", "value": "close"})
    )

    if tosqlite:
        # Create sqlite database connection object
        try:
            conn = sqlite3.connect(database_name)
        except sqlite3.OperationalError:
            conn = sqlite3.connect(database_name)
            conn.execute("CREATE TABLE prices (date DATE, symbol TEXT, close FLOAT)")

        # Write dataframe to a table in sqlite database
        data.to_sql("prices", conn, if_exists="replace", index=False)

        # Close connection object
        conn.close()
    else:
        return data


if __name__ == "__main__":
    portfolio_string = ["SPY WMT JNPR CVS BAC JNJ ABBNY SHEL ORCL USRT"]
    data_loader(portfolio=portfolio_string)
