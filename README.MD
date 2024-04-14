# Hedging HKEX Listed Warrants (MH:4514 Financial Mathematics)

Please Star ⭐️ the repo, if you find it helpful....

The repository helps to maintain and create a self-financing portoflio using Delta hedging to hedge warrants listed on Hong Kong Exchange (HKEX). It uses Black Scholes formula and Implied Volatility.

It supports all warrants listed on HKEX. 

- Data Collection : All data collection is embedded in the repository. It only requires the warrant code as mentioned in the HKEX listing.

- Warrant : Supports different entitlement ratios and both call and put options.

- Implied Volatility : If no estimate for volatility is provided, we calculate the implied volaity using Black Scholes and Current Market Price of the Warrant


## Future work

- Implied Volatility Smile : Use various warrant of same eunderlying asset listed on HKEX with different Strike Prices and Matruity dates to build a volatility smile curve for better estimate of IV.