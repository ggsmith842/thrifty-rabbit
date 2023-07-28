"""
Provides goal-based investing support. Takes in client
input and returns a bucketed portfolio recommendation
based on risk tolerance and risk capacity.
"""

#!/usr/bin/env python #
from datetime import date
import pandas as pd


class Goal:
    '''
    Goal class holds goal based answer to client questionairre.
    '''
    def __init__(
        self,
        name,
        target_year,
        target_value,
        initial_contribution=0,
        monthly_contribution=0,
        priority="",
    ):
        self.name = name
        self.target_year = target_year
        self.target_value = target_value
        self.initial_contribution = initial_contribution
        self.monthly_contribution = monthly_contribution
        if  (priority != "") and (
            priority not in ["Dreams", "Wishes", "Wants", "Needs"]
        ):
            raise ValueError("Wrong value set for Priority.")
        self.priority = priority

    def get_goal_probabilities(self):
        '''
        Calculates the probability of reaching a goal.
        '''
        if self.priority == "":
            raise ValueError("No value set for Priority.")
        lookup_table = pd.read_csv("../Data/goalprobabilities.csv")
        match = lookup_table["Realize"] == self.priority
        min_prob = lookup_table["MinP"][(match)]
        max_prob = lookup_table["MaxP"][(match)]
        return min_prob.values[0], max_prob.values[0]


class RetirementGoal(Goal):
    '''
    Holds information for specific goal of type retirement.
    '''
    def __init__(self, name, target_value, startingAge, retirementAge):
        target_year = date.today().year + (retirementAge - startingAge)
        super().__init__(name, target_year, target_value)
        self.retirement_age = retirementAge


class GrowWelathGoal(Goal):
    '''
    Holds information for specific goal of type grow wealth.
    '''
    def __init__(self, initial_contribution, monthly_contribution):
        target_year = date.today().year + 10
        target_amount = 1000000
        super().__init__(
            "Grow My Wealth",
            target_year,
            target_amount,
            initial_contribution,
            monthly_contribution,
        )
