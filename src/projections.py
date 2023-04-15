# #!/usr/bin/env python # 

class Projection:
  def __init__(self, expectedReturn: float, expectedRisk: float, initialInvestment: float, monthlyInvestment: float, years: int):
    from datetime import date
    import pandas as pd
    df = pd.DataFrame({'date': [],
                    'lowValue': [],
                    'value': [],
                    'highValue': []})
    df.set_index('date')

    for year in range(years+1):
      newValue = self.returnProjection(expectedReturn, initialInvestment, monthlyInvestment, year)
      newValueLower = self.returnProjection(expectedReturn-expectedRisk, initialInvestment, monthlyInvestment, year)
      newValueUpper = self.returnProjection(expectedReturn+expectedRisk, initialInvestment, monthlyInvestment, year)
      newDate = date.today()
      newDate = newDate.replace(year=newDate.year + year)
      newRow = pd.Series({'date': newDate, 'lowValue': newValueLower, 'value': newValue, 'highValue': newValueUpper},name='')
      df = pd.concat([df, newRow.to_frame().T],axis=0)
    
    df = df.set_index(pd.DatetimeIndex(df['date']))
    df = df.drop(columns="date")
    self.data = df

  @staticmethod
  def returnProjection(expectedReturn, initialInvestment, monthlyInvestment, years):
    valuePrincipal = initialInvestment * pow(1 + expectedReturn/12, (years*12))
    valueMonthly = monthlyInvestment * (pow(1 + expectedReturn/12, (years*12))-1)/(expectedReturn/12)
    return valuePrincipal+valueMonthly

  def visualize(self, targetAmount: float = 0.0):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    scale_y = 1e6
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
    fig, ax=plt.subplots()
    ax.yaxis.set_major_formatter(ticks_y)
    ax.set_ylabel('Millions (USD)')
    ax.plot(self.data.index, self.data['highValue'], label="High")
    ax.plot(self.data.index, self.data['value'], label="Expected")
    ax.plot(self.data.index, self.data['lowValue'], label="Low")
    plt.legend(loc="upper left")
    if (targetAmount > 0):
      plt.axhline(y=targetAmount)
    fig.tight_layout()
    plt.show()