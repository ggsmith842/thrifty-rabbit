"""
Provides classes for building an investment portfolio
"""
#!/usr/bin/env python
import matplotlib.pyplot as plt

import pandas as pd
import yfinance as yf

from pypfopt import plotting
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier

import numpy as np


class Allocation:
    """
    Helper class used in Portfolio
    """

    def __init__(self, asset_ticker, percentage):
        self.ticker = asset_ticker
        self.percentage = percentage


class Portfolio:
    """
    Portolio class that holds pricing data for each asset,
    performs optimization calculations, and returns reports to the user.
    """

    def __init__(
        self,
        ticker_string: str,
        expected_return: float,
        portfolio_name: str,
        risk_bucket: int,
    ):
        self.name = portfolio_name
        self.risk_bucket = risk_bucket
        self.expected_return = expected_return
        self.allocations = []

        price_df = self.__get_daily_prices(ticker_string, "20y")

        self.mu = expected_returns.mean_historical_return(price_df)
        self.S = risk_models.sample_cov(price_df)

        self.efficient_frontier = EfficientFrontier(self.mu, self.S)

        self.efficient_frontier.efficient_return(expected_return)
        self.expected_risk = self.efficient_frontier.portfolio_performance()[1]
        portfolio_weights = self.efficient_frontier.clean_weights()

        for key, value in portfolio_weights.items():
            new_allocation = Allocation(key, value)
            self.allocations.append(new_allocation)

    def __get_daily_prices(self, ticker_string_list, period):
        data = yf.download(ticker_string_list, group_by="Ticker", period=period)
        data = data.iloc[:, data.columns.get_level_values(1) == "Close"]
        data = data.dropna()
        data.columns = data.columns.droplevel(1)
        return data

    @staticmethod
    def get_portfolio_mapping(risk_tolerance_score, risk_capacity_score):
        """
        Maps a portfolio to a risk tolerance and capacity bucket.
        """
        allocation_lookup_table = pd.read_csv("../Data/riskbuckets.csv")
        match_tol = (
            allocation_lookup_table["ToleranceMin"] <= risk_tolerance_score
        ) & (allocation_lookup_table["ToleranceMax"] >= risk_tolerance_score)
        match_cap = (allocation_lookup_table["CapacityMin"] <= risk_capacity_score) & (
            allocation_lookup_table["CapacityMax"] >= risk_capacity_score
        )
        portfolio_id = allocation_lookup_table["Portfolio"][(match_tol & match_cap)]
        return portfolio_id.values[0]

    def get_class_alloc(self):
        """
        Returns a dataframe with the asset
        and its optimal weight in the portfolio
        """
        asset_class_weights = []
        asset_class_labels = []

        for asset in self.allocations:
            asset_class_weights.append(asset.percentage)
            asset_class_labels.append(asset.ticker)

        alloc_df = (
            pd.DataFrame(
                zip(asset_class_labels, asset_class_weights), columns=["Type", "Weight"]
            )
            .groupby("Type")
            .sum()
            .reset_index()
        )
        return alloc_df

    def get_market(self):
        """
        Returns a dataframe with market information for an asset.
        """
        asset_class_weights = []
        asset_class_labels = []

        for asset in self.allocations:
            try:
                asset_mkt = yf.Ticker(asset.ticker).info["country"]
            except KeyError:
                asset_mkt = "N/A"
            asset_class_weights.append(asset.percentage)
            asset_class_labels.append(asset_mkt)

        market_df = (
            pd.DataFrame(asset_class_labels, asset_class_weights)
            .reset_index()
            .rename(columns={0: "region", "index": "weight"})
            .groupby("region")
            .sum()
        )

        return market_df

    def show_efficient_frontier(self):
        """
        Plots the efficient frontier for a given set of expected returns.

        Returns:
            None
        """
        efficient_frontier = EfficientFrontier(self.mu, self.S)
        _, ax = plt.subplots()
        ef_max_sharpe = EfficientFrontier(self.mu, self.S)
        ef_return = EfficientFrontier(self.mu, self.S)
        plotting.plot_efficient_frontier(efficient_frontier, ax=ax, show_assets=False)
        n_samples = 10000
        weights = np.random.dirichlet(np.ones(efficient_frontier.n_assets), n_samples)
        rets = weights.dot(efficient_frontier.expected_returns)
        stds = np.sqrt(np.diag(weights @ efficient_frontier.cov_matrix @ weights.T))
        sharpes = rets / stds
        ax.scatter(stds, rets, marker=".", c=sharpes, cmap="viridis_r")
        ef_max_sharpe.max_sharpe()
        ret_tangent, std_tangent, _ = ef_max_sharpe.portfolio_performance()
        ax.scatter(
            std_tangent, ret_tangent, marker="*", s=100, c="r", label="Max Sharpe"
        )
        ef_return.efficient_return(self.expected_return)
        ret_tangent2, std_tangent2, _ = ef_return.portfolio_performance()
        return_p = str(int(self.expected_return * 100)) + "%"
        ax.scatter(std_tangent2, ret_tangent2, marker="*", s=100, c="y", label=return_p)
        ax.set_title(f"Efficient Frontier for {return_p} returns")
        ax.legend()
        plt.tight_layout()
        plt.show()
