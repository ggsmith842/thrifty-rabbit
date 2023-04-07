# thrifty-rabbit

![Logo](https://github.com/ggsmith842/thrifty-rabbit/blob/main/thirfyRabbit.jpg?raw=true)


### Goals:
1. Monitor a dividend-focused portfolio for performance and health.
2. Create an optimized portfolio by creating a robo-advisor with an objective of maximizing long-term returns 

#### 1. Monitoring

How will this be done?

1. For a given portfolio collect the fundamentals. This is done with the Alpha Vantage API
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

(Coming soon)



### Data Model

(Coming soon)
