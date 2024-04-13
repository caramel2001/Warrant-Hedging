import pandas as pd
import pandas_market_calendars as mcal


def get_trading_days(start_date:str, end_date:str, exchange="HKEX"):
    # Create a calendar for the HKEX
    hkex_calendar = mcal.get_calendar(exchange)
    # Get the trading days between the start and end date
    hkex_trading_days = hkex_calendar.valid_days(start_date=start_date, end_date=end_date)

    # Calculate the number of trading days
    number_of_trading_days = len(hkex_trading_days)

    number_of_trading_days