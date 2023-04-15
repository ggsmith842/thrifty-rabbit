#!/usr/bin/env python # 
import pandas as pd
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
import yfinance as yf


class Allocation:
    def __init__(self, ticker, percentage):
        self.ticker = ticker
        self.percentage = percentage
    
class Portfolio:
    def __init__(self, tickerString: str, expectedReturn: float, portfolioName: str, riskBucket: int):

        self.name = portfolioName
        self.riskBucket = riskBucket
        self.expectedReturn = expectedReturn
        self.allocations = []

        from pypfopt.efficient_frontier import EfficientFrontier
        from pypfopt import risk_models
        from pypfopt import expected_returns

        df = self.__getDailyPrices(tickerString, "20y")

        mu = expected_returns.mean_historical_return(df)
        S = risk_models.sample_cov(df)

        ef = EfficientFrontier(mu, S)

        ef.efficient_return(expectedReturn)
        self.expectedRisk = ef.portfolio_performance()[1]
        portfolioWeights = ef.clean_weights()

        for key, value in portfolioWeights.items():
            newAllocation = Allocation(key, value)
            self.allocations.append(newAllocation)

    def __getDailyPrices(self, tickerStringList, period):
        data = yf.download(tickerStringList, group_by="Ticker", period=period)
        data = data.iloc[:, data.columns.get_level_values(1)=="Close"]
        data = data.dropna()
        data.columns = data.columns.droplevel(1)
        return data
    
    @staticmethod
    def getPortfolioMapping(riskToleranceScore, riskCapacityScore):
        import pandas as pd
        allocationLookupTable=pd.read_csv('../Data/riskbuckets.csv')
        matchTol = (allocationLookupTable['ToleranceMin'] <=  riskToleranceScore) & (allocationLookupTable['ToleranceMax'] >=  riskToleranceScore)
        matchCap = (allocationLookupTable['CapacityMin'] <=  riskCapacityScore) & (allocationLookupTable['CapacityMax'] >=  riskCapacityScore)
        portfolioID = allocationLookupTable['Portfolio'][(matchTol & matchCap)]
        return portfolioID.values[0]
    
    def get_class_alloc(self):
        asset_class_weights = []
        asset_class_labels = []
        
        for asset in self.allocations:
            asset_class_weights.append(asset.percentage)                        
            asset_class_labels.append(asset.ticker)

        df = pd.DataFrame(zip(asset_class_labels,asset_class_weights),columns=["Type","Weight"]).groupby('Type').sum().reset_index()
        return df

    def get_market(self):
        import yfinance as yf
        asset_class_weights = []
        asset_class_labels = []
         
        for asset in self.allocations:
             asset_mkt = yf.Ticker(asset.ticker).info['market']
             asset_class_weights.append(asset.percentage)
             asset_class_labels.append(asset_mkt)

        df = pd.DataFrame(asset_class_labels, asset_class_weights).reset_index().rename(columns={0:"region","index":"weight"}).groupby("region").sum()
        
        return df
    
    
    def show_efficient_frontier(self):
        import numpy as np
        from pypfopt import plotting

        ef = EfficientFrontier(self.mu, self.S)
        fix, ax = plt.subplots()
        ef_max_sharpe = EfficientFrontier(self.mu, self.S)
        ef_return = EfficientFrontier(self.mu, self.S)
        plotting.plot_efficient_frontier(ef, ax=ax, show_assets=False)
        n_samples = 10000
        w = np.random.dirichlet(np.ones(ef.n_assets), n_samples)
        rets = w.dot(ef.expected_returns)
        stds = np.sqrt(np.diag(w @ ef.cov_matrix @ w.T))
        sharpes = rets / stds
        ax.scatter(stds, rets, marker=".", c=sharpes,
            cmap="viridis_r")
        ef_max_sharpe.max_sharpe()
        ret_tangent, std_tangent, _ = ef_max_sharpe.portfolio_performance()
        ax.scatter(std_tangent, ret_tangent, marker="*", s=100,
            c="r", label="Max Sharpe")
        ef_return.efficient_return(self.expectedReturn)
        ret_tangent2, std_tangent2, _ = ef_return.portfolio_performance()
        returnP = str(int(self.expectedReturn*100))+"%"
        ax.scatter(std_tangent2, ret_tangent2, marker="*", s=100,
            c="y", label=returnP)
        ax.set_title(f"Efficient Frontier for {returnP} returns")
        ax.legend()
        plt.tight_layout()
        plt.show()


class Evaluator:
    def __init__(self, ticker):
        self.ticker = ticker
        import yfinance as yf   
        import pandas as pd   
        data = yf.download(ticker,period='10y')
        data = pd.DataFrame(data['Close'])

        self.data = data

    def data(self):
        return self.data
    
    def expected(self):
        from pypfopt.efficient_frontier import EfficientFrontier
        from pypfopt import risk_models
        from pypfopt import expected_returns
        df = self.data
        mu = expected_returns.mean_historical_return(df)
        S = risk_models.sample_cov(df)
        ef = EfficientFrontier(mu, S)

        return mu, S, ef

            
