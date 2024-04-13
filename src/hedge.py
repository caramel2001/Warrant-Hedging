import numpy as np
from scipy.stats import norm
from tqdm import tqdm

def black_scholes_call(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes call option price and delta.

    Parameters:
    S - current stock price
    K - option strike price
    T - time to maturity
    r - risk-free interest rate
    sigma - volatility of the underlying stock

    Returns:
    call_price - price of the call option
    delta - delta of the call option
    """
    # Calculate d1 and d2
    S = round(S, 5)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d1 = round(d1, 5)
    d2 = d1 - sigma * np.sqrt(T)
    d2 = round(d2, 5)
    # Call option price
    call_price = S * round(norm.cdf(d1),5) - K * np.exp(-r * T) * round(norm.cdf(d2),5)

    # Delta of the call option
    delta = norm.cdf(d1)

    return call_price, delta

def black_scholes_put(S, K, T, r, sigma):   
    """
    Calculate the Black-Scholes put option price and delta.

    Parameters:
    S - current stock price
    K - option strike price
    T - time to maturity
    r - risk-free interest rate
    sigma - volatility of the underlying stock

    Returns:
    put_price - price of the put option
    delta - delta of the put option
    """
    # Calculate d1 and d2
    S = round(S, 5)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d1 = round(d1, 5)
    d2 = d1 - sigma * np.sqrt(T)
    d2 = round(d2, 5)
    # Put option price
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    # Delta of the put option
    delta = norm.cdf(d1) - 1

    return put_price, delta

def vega(S, K, T, r, sigma):
    '''
    :param S: Asset price
    :param K: Strike price
    :param T: Time to Maturity
    :param r: risk-free rate (treasury bills)
    :param sigma: volatility
    :return: partial derivative w.r.t volatility
    '''
    N_prime = norm.pdf

    ### calculating d1 from black scholes
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))

    
    vega = S  * np.sqrt(T) * N_prime(d1)
    return vega

def implied_volatility_put(P, S, K, T, r, tol=0.00001):
    '''
    :param P: Observed put price
    :param S: Asset price
    :param K: Strike Price
    :param T: Time to Maturity
    :param r: riskfree rate
    :param tol: error tolerance in result
    :return: implied volatility in percent
    '''
    sigma = 0.3
    for i in tqdm(range(100)):
        ### calculate
        diff = black_scholes_put(S, K, T, r, sigma)[0] - P
        if abs(diff) < tol:
            print(f'found on {i}th iteration')
            print(f'difference is equal to {diff}')
            break
        sigma = sigma - diff / vega(S, K, T, r, sigma)
    return sigma

def implied_volatility_call(C, S, K, T, r, tol=0.00001,
                            max_iterations=100):
    '''
    :param C: Observed call price
    :param S: Asset price
    :param K: Strike Price
    :param T: Time to Maturity
    :param r: riskfree rate
    :param tol: error tolerance in result
    :param max_iterations: max iterations to update vol
    :return: implied volatility in percent
    '''
    sigma = 0.3
    for i in tqdm(range(max_iterations)):
        ### calculate difference between blackscholes price and market price with
        ### iteratively updated volality estimate
        diff = black_scholes_call(S, K, T, r, sigma)[0] - C
        ###break if difference is less than specified tolerance level
        if abs(diff) < tol:
            print(f'found on {i}th iteration')
            print(f'difference is equal to {diff}')
            break
        ### use newton rapshon to update the estimate
        sigma = sigma - diff / vega(S, K, T, r, sigma)
    return sigma