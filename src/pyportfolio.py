#!/usr/bin/env python # 
import pandas as pd
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier


#portfolio class
class Portfolio:
    def __init__(self, name, tickers:str, riskBucket, expectedReturn = 0, expectedRisk=0):
        self.name = name
        self.riskBucket = riskBucket
        self.allocations = []
        self.expectedReturn = expectedReturn
        self.tickers = tickers
  
        from pypfopt.efficient_frontier import EfficientFrontier
        from pypfopt import risk_models
        from pypfopt import expected_returns
        df = self.__get_closing_prices(tickers)
        mu = expected_returns.mean_historical_return(df)
        S = risk_models.sample_cov(df)
        ef = EfficientFrontier(mu, S)
        ef.efficient_return(expectedReturn)
        portfolioWeights = ef.clean_weights() 
        for key, value in portfolioWeights.items():
            newAllocation = Allocation(key,value)
            self.allocations.append(newAllocation)  

        self.mu = mu
        self.S = S
        self.ef = ef
    

    def print_portfolio(self):
        
        #portfolio metadata
        print(f'Portfolio Name: {self.name}\nRisk bucket: {str(self.riskBucket)}\nExpected Return: {self.expectedReturn:.2%}')
        
        #portfolio allocation
        print(f'\nAllocations:')
        for allocation in self.allocations:
            print(f"Asset: {allocation.ticker}; Percent of Portfolio: {allocation.percentage:.2%}")
        #expected performance
        print("\nExpected Performance:")
        self.ef.portfolio_performance(verbose=True)
        

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
    
    def __get_closing_prices(self,tickers,period="20y"):
        import yfinance as yf
       
        data = yf.download(tickers, group_by="Ticker" ,period=period)

        data = data.iloc[:,data.columns.get_level_values(1)=="Close"]
        data.dropna(inplace=True)
        data.columns = data.columns.droplevel(1)

        return data
    
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
        ax.set_title("Efficient Frontier for " + returnP +           " returns")
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



    


            
#allocation
class Allocation:
    '''
    An allocation is an asset such as a stock or bond
    '''
    def __init__(self,ticker,percentage):
        self.ticker = ticker
        self.percentage = percentage

