#!/usr/bin/env python # 
from datetime import date
import pandas as pd

class Goal:
  def __init__(self, name, targetYear, targetValue, initialContribution=0, monthlyContribution=0, priority=""):
    self.name = name
    self.targetYear = targetYear
    self.targetValue = targetValue
    self.initialContribution = initialContribution
    self.monthlyContribution = monthlyContribution
    if not (priority == "") and not (priority in ["Dreams", "Wishes", "Wants", "Needs"]):
            raise ValueError('Wrong value set for Priority.')
    self.priority = priority

  def getGoalProbabilities(self):
    if (self.priority == ""):
            raise ValueError('No value set for Priority.')
    import pandas as pd
    lookupTable=pd.read_csv('../Data/goalprobabilities.csv') 
    match = (lookupTable['Realize'] == self.priority)
    minProb = lookupTable['MinP'][(match)]
    maxProb = lookupTable['MaxP'][(match)]
    return minProb.values[0], maxProb.values[0]
    
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