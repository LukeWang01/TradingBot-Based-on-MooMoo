import datetime
import pandas_market_calendars as mcal


def is_trading_day():
    # Get today's date
    today = datetime.datetime.now().date()

    # Specify the market calendar (e.g., 'XNYS' for New York Stock Exchange)
    nyse = mcal.get_calendar('XNYS')

    # Check if today is a valid trading day
    # return yes if today is a trading day, no if not.
    return nyse.valid_days(start_date=today, end_date=today).size > 0


def check_if_weekday():
    tmp = datetime.datetime.now().date()
    if tmp.weekday() < 5:
        print("Today is a workday, running the bot")
        return True
    else:
        print("Today is not a workday, skip the bot.")
        return False


def is_market_hours():
    current_time = datetime.datetime.now().time()
    market_open_time = datetime.time(9, 30)  # Regular market open time (9:30 AM)
    market_close_time = datetime.time(16, 0)  # Regular market close time (4:00 PM)

    if market_open_time <= current_time <= market_close_time:
        return True
    else:
        return False


def is_market_and_extended_hours():
    current_time = datetime.datetime.now().time()
    trade_open_time = datetime.time(4, 0)  # Regular market open time (4:00 AM)
    trade_close_time = datetime.time(20, 0)  # Regular market close time (20:00 PM)

    if trade_open_time <= current_time <= trade_close_time:
        return True
    else:
        return False