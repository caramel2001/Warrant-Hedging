from scipy.stats import norm
import numpy as np
from hedge import implied_volatility_call, implied_volatility_put
class Option:
    def __init__(self,C,S,K,T,r,sigma=None,call=True) -> None:
        self.C = C
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        if sigma is None:
            # calculate implied volatility
            if call:
                sigma = implied_volatility_call(C,S,K,T,r)
            else:
                sigma = implied_volatility_put(C,S,K,T,r)
        self.sigma = sigma

    def call(self):
        S = round(self.S, 5)
        d1 = (np.log(S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d1 = round(d1, 5)
        d2 = d1 - self.sigma * np.sqrt(self.T)
        d2 = round(d2, 5)
        call_price = S * round(norm.cdf(d1),5) - self.K * np.exp(-self.r * self.T) * round(norm.cdf(d2),5)
        delta = norm.cdf(d1)
        return call_price, delta
    
    def put(self):
        S = round(self.S, 5)
        d1 = (np.log(S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d1 = round(d1, 5)
        d2 = d1 - self.sigma * np.sqrt(self.T)
        d2 = round(d2, 5)
        put_price = self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1
        return put_price, delta
    

class Warrant(Option):
    """Warrent class that inherits from Option class from HKEX Warrants"""
    def __init__(self, C, S, K, T, r, sigma=None, call=True,entitlement=1) -> None:
        super().__init__(C, S, K, T, r, sigma, call)
        self.entitlement = entitlement

    def call(self):
        return super().call()/self.entitlement
    
    def put(self):
        return super().put()/self.entitlement