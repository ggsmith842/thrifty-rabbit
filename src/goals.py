#!/usr/bin/env python # 
from datetime import date

class Goal:
    def __init__(self, name, targetYear, targetValue, initialContribution=0, monthlyContribution=0):
        self.name = name
        self.targetYear = targetYear
        self.targetValue = targetValue
        self.initialContribution = initialContribution
        self.monthlyContribution = monthlyContribution

class RetirementGoal(Goal):
    def __init__(self, name, targetValue, startingAge, retirementAge):
        targetYear = date.today().year + (retirementAge-startingAge)
        super().__init__(name, targetYear,targetValue)
        self.retirementAge = retirementAge

class GrowWelathGoal(Goal):
    def __init__(self,initialContribution, monthlyContribution):
        targetYear = date.today().year + 10
        targetAmount = 1000000
        super().__init__("Grow My Wealth", targetYear, targetAmount, initialContribution, monthlyContribution)