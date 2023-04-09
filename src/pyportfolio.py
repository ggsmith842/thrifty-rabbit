import pandas as pd
import yfinance as yf


#portfolio class
class Portfolio:
    def __init__(self, name, riskBucket, exprectedReturn = 0, expectedRisk=0):
        self.name = name
        self.riskBucket = riskBucket
        self.allocations = []
        self.expectedReturn = exprectedReturn

    def get_class_alloc(self):
        asset_class_weights = []
        asset_class_labels = []
        
        for asset in self.allocations:
            asset_class_weights.append(asset.percentage)                        
            asset_class_labels.append(asset.asset_class)

        df = pd.DataFrame(zip(asset_class_labels,asset_class_weights),columns=["Type","Weight"]).groupby('Type').sum().reset_index()
        return df

    def get_market(self):
        asset_class_weights = []
        asset_class_labels = []
         
        for asset in self.allocations:
             asset_mkt = yf.Ticker(asset.ticker).info['market']
             asset_class_weights.append(asset.percentage)
             asset_class_labels.append(asset_mkt)

        df = pd.DataFrame(asset_class_labels, asset_class_weights).reset_index().rename(columns={0:"region","index":"weight"}).groupby("region").sum()
        
        return df
    
    def get_closing_prices(self,period="20y"):
        tickers = ""
        for allocation in self.allocations:
            tickers += str(allocation.ticker) + " "

        data = yf.download(tickers, group_by="Ticker" ,period=period)

        data = data.iloc[:,data.columns.get_level_values(1)=="Close"]
        data.dropna(inplace=True)
        data.columns = data.columns.droplevel(1)

        return data
            


             
#allocation
class Allocation:
    '''
    An allocation is an asset such as a stock or bond
    '''
    def __init__(self,ticker,percentage,asset_class):
        self.ticker = ticker
        self.percentage = percentage
        self.asset_class = asset_class
