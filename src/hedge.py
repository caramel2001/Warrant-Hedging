from .data import DataSource
from .warrant import Warrant
from .utils import get_trading_days
import pandas as pd
class HedgePortfolio:
    def __init__(self,warrant:DataSource,r = 0.00,start_date = None) -> None:
        """Portoflio class to hedge warrant with underlying stock, it is self-financing.

        Args:
            warrant (DataSource): DataSource Object
            r (float, optional): Risk free rate. Defaults to 0.00.
        """
        self.riskless = None
        self.stock = None
        self.warrant = warrant
        self.warrant.get_data()
        self.r = r

    def get_T(self,start_date = None):
        maturity = self.warrant.info_df['Maturity Date(D/M/Y)']
        maturity = pd.to_datetime(maturity, format='%d/%m/%Y').date()
        start_date = start_date or self.warrant.price_df.iloc[0]['sdate2']
        start_date = pd.to_datetime(start_date, format='%d/%m/%Y').date()
        return get_trading_days(start_date,maturity)/252
    
    def get_warrant_option(self,date) -> Warrant:
        T = self.get_T(start_date=date)
        temp = self.warrant.price_df.set_index('sdate2').copy()
        print("Warrant price: ",temp['wlast'].loc[date])
        C = float(temp['wlast'].loc[date])
        S = float(temp['ulast'].loc[date])
        K = float(self.warrant.info_df['Strike(HKD)'])
        warrant = Warrant(C,S,K,T,self.r,sigma = None, # calculates Implied volatility
            call = self.warrant.info_df['Type'] == 'Call',
            entitlement=float(self.warrant.info_df['Conversion Ratio'])
        )
        return warrant

    def initialize_portfolio(self,start_date = None):
        """Initialize the portfolio with the warrant and riskless asset
        
        Args:
            start_date (str, optional): Start date of the portfolio in D/M/Y format. Defaults to None that means the Current last trading date of the warrant.
        """
        warrant = self.get_warrant_option(start_date)
        _, delta = warrant()
        self.stock = delta
        self.riskless = float(warrant.C - delta * warrant.S)
        self.summary(start_date)

    def update_portfolio(self):
        date = self.warrant.price_df['sdate2'].iloc[0]
        warrant = self.get_warrant_option(date=date)
        v0 = self.stock * float(self.warrant.price_df['ulast'].iloc[0]) + self.riskless # current value of portfolio
        _, delta = warrant()
        self.stock = delta
        self.riskless = v0 - delta * float(self.warrant.price_df['ulast'].iloc[0])
        self.summary()

    def summary(self,start_date = None):
        print("------Portfolio Summary------")
        print(f"Stock Units: {self.stock}")
        print(f"Riskless Units: {self.riskless}")
        if self.stock is not None and self.riskless is not None:
            if start_date is not None:
                S = float(self.warrant.price_df.set_index('sdate2').loc[start_date]['ulast'])
            else:
                S = float(self.warrant.price_df['ulast'].iloc[0])
            print(f"Current Portfolio Value: {self.stock * S + self.riskless}")
        print("----------------------------")



