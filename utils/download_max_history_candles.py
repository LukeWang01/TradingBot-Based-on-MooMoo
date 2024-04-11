import datetime

from quoter.quoter_Webull import Quoter_Webull
from quoter.quoter_Yahoo import Quoter_Yahoo
from utils.dataIO import save_to_csv, save_to_xls, save_to_json, logging_error

""" 
Download stock history data:

1. Define stock list below, type the tickers you want to download
2. Run this script
3. Data will be saved in ../data/ticker_name/

OR, you can modify the functions to save whatever you want.

Note: 
    1min, 2min, 1h, 1d data are from Yahoo, 5min, 15min, 30min data are from Webull.
    Download max history data by default, it may take about 2 minutes, please be patient.

"""


def download_max_history_candles(stock, count='max', save_format='csv'):
    """
        :param stock: ticker
        :param count: max 1200 for 1d
        :param save_format: 'csv' or 'xls'
        :return: pandas dataframe
        """

    yh_quoter = Quoter_Yahoo()
    wb_quoter = Quoter_Webull()

    stock = stock.upper()
    response_1h_bar = yh_quoter.get_1h_bar(stock=stock, count=count, extend_trading=True)
    response_1d_bar = yh_quoter.get_1d_bar(stock=stock, count=count, extend_trading=False)

    save_dir = f'data/{stock}/'
    current_date = datetime.datetime.today().strftime('%Y%m%d')

    if response_1h_bar.empty and response_1d_bar.empty:
        logging_error('Invalid ticker or interval')
    else:
        if save_format == 'csv':
            save_to_csv(save_dir, f'{stock}_{current_date}_1h', response_1h_bar)
            save_to_csv(save_dir, f'{stock}_{current_date}_1d', response_1d_bar)
        elif save_format == 'xls':
            save_to_xls(save_dir, f'{stock}_{current_date}_1h', response_1h_bar)
            save_to_xls(save_dir, f'{stock}_{current_date}_1h', response_1d_bar)
        elif save_format == 'json':
            save_to_json(save_dir, f'{stock}_{current_date}_1h', response_1h_bar)
            save_to_json(save_dir, f'{stock}_{current_date}_1h', response_1d_bar)
