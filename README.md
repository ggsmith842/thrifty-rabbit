# thrifty-rabbit

[![Pylint](https://github.com/ggsmith842/thrifty-rabbit/actions/workflows/pylint.yml/badge.svg)](https://github.com/ggsmith842/thrifty-rabbit/actions/workflows/pylint.yml)

![Logo](https://github.com/ggsmith842/thrifty-rabbit/blob/main/thirfyRabbit.jpg?raw=true)



### Goals:
1. Monitor a portfolio for performance and health.
2. Optimize a portfolio by creating a robo-advisor with an objective of maximizing long-term returns.

#### 1. Monitoring

How will this be done?

1. Collect fundamental data for assets in the portfolio using the [yfinance](https://pypi.org/project/yfinance/) package.
2. Calculate metrics used to evaluate a stock for a dividend portfolio
    - Yield (%)
    - Dividend Payout Ratio
    - Dividend Coverage Ratio
    - Free Cash Flow to Equity
    - Net Debt to EBIDTA Ratio
    - BETA (Volatitlity)
3. Establish rules determining the health of the assets in the portfolio. Examples are:
    - a company stops paying a dividend
    - a dividend yield has steadily descrased for 2 quarters
    - a company is low on cash
4. Develop a portfolio health score and thresholds using the rules and metrics established above
5. Visualize and report results
6. Automate reporting and data refreshes.

#### 2. Automate and Optimize

1. Using [pyportfolioopt](https://pypi.org/project/pyportfolioopt/)

(Coming soon)



### Data Model

(Coming soon)
