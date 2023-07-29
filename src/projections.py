"""
This module is used to visualize projections based on a portfolio's expected return. 
"""

#!/usr/bin/env python #

from datetime import date
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class Projection:
    """
    Class that performs calcaultions needed to forecast projected returns.
    """

    def __init__(
        self,
        expected_return: float,
        expected_risk: float,
        initial_investment: float,
        monthly_investment: float,
        years: int,
    ):
        projection_df = pd.DataFrame(
            {"date": [], "lowValue": [], "value": [], "highValue": []}
        )
        projection_df.set_index("date")

        for year in range(years + 1):
            new_value = self.return_projection(
                expected_return, initial_investment, monthly_investment, year
            )
            new_value_lower = self.return_projection(
                expected_return - expected_risk,
                initial_investment,
                monthly_investment,
                year,
            )
            new_value_upper = self.return_projection(
                expected_return + expected_risk,
                initial_investment,
                monthly_investment,
                year,
            )
            new_date = date.today()
            new_date = new_date.replace(year=new_date.year + year)
            new_row = pd.Series(
                {
                    "date": new_date,
                    "lowValue": new_value_lower,
                    "value": new_value,
                    "highValue": new_value_upper,
                },
                name="",
            )
            projection_df = pd.concat([projection_df, new_row.to_frame().T], axis=0)

        projection_df = projection_df.set_index(pd.DatetimeIndex(projection_df["date"]))
        projection_df = projection_df.drop(columns="date")
        self.data = projection_df

    @staticmethod
    def return_projection(
        expected_return, initial_investment, monthly_investment, years
    ):
        """
        Returns the forcasted value for the portfolio.
        """
        value_principal = initial_investment * pow(
            1 + expected_return / 12, (years * 12)
        )
        value_monthly = (
            monthly_investment
            * (pow(1 + expected_return / 12, (years * 12)) - 1)
            / (expected_return / 12)
        )
        return value_principal + value_monthly

    def visualize(self, target_amount: float = 0.0):
        """
        Plots the projection using matplotlib
        """

        scale_y = 1e6
        ticks_y = ticker.FuncFormatter(lambda x, pos: f"{x / scale_y:g}")
        # ticks_y = ticker.FuncFormatter(lambda x, pos: "{0:g}".format(x / scale_y))
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(ticks_y)
        ax.set_ylabel("Millions (USD)")
        ax.plot(self.data.index, self.data["highValue"], label="High")
        ax.plot(self.data.index, self.data["value"], label="Expected")
        ax.plot(self.data.index, self.data["lowValue"], label="Low")
        plt.legend(loc="upper left")
        if target_amount > 0:
            plt.axhline(y=target_amount)
        fig.tight_layout()
        plt.show()
