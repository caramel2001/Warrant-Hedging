import requests
import pandas as pd
from matplotlib import pyplot as plt

class DataSource:
    """Base class for data source. 
    Args:
        warrant_code (str): Warrant code based on HKEX listing
    """
    def __init__(self, warrant_code) -> None:
        self.warrant_code = warrant_code
    
    def get_data(self):
        raise NotImplementedError

    def price_plot(self):
        raise NotImplementedError
    
    def get_price(self):
        raise NotImplementedError
    
    def get_info(self):
        raise NotImplementedError


class BOCI(DataSource):
    """DataSource class using BOCI Data"""
    def __init__(self,warrant_code) -> None:
        super().__init__(warrant_code)

    def get_data(self,plot=True):
        self.info_df = self.get_info()
        print(self.info_df.to_markdown())
        price = self.get_price()
        self.price_df = pd.DataFrame(price['data']).transpose()
        self.price_df['sdate'] = pd.to_datetime(self.price_df['sdate'])
        if plot:
            fig = self.price_plot()
            fig.show()
        
    def price_plot(self):
        fig, ax1 = plt.subplots(figsize=(10, 5))
        self.price_df.set_index('sdate')['ulast'].astype(float).plot(ax=ax1, color='r',ylabel='underlying price', title='Underlying and Warrant Price',label='underlying price')
        ax2 = ax1.twinx()
        self.price_df.set_index('sdate')['wlast'].astype(float).plot(ax=ax2, color='b',ylabel='warrant price',label='warrant price')
        # plt.legend(['underlying price', 'warrant price'])
        fig.legend()
        return fig

    def get_price(self):
        resp = requests.get(f"https://www.bocifp.com/home/chart/warrant_chart.php?code={self.warrant_code}&action=json", headers={'User-Agent': 'Mozilla/5.0'})

        return resp.json()
    
    def get_info(self):
        info_df = pd.read_html(f"https://www.bocifp.com/en/warrant/warrant-indicator/code/{self.warrant_code}")[2]
        info_df = info_df.set_index(0)
        info_df=pd.concat([info_df[1],info_df.set_index(2)[3]], axis=0)
        return info_df