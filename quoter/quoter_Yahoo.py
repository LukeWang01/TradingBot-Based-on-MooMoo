import yfinance as yf

from quoter.Quoter import Quoter
from utils.dataIO import logging_info, logging_error


class Quoter_Yahoo(Quoter):
    def __init__(self):
        super().__init__()
        self.name = "Yahoo Platform"
        logging_info('Quoter_Yahoo created')

    """
        Limit:  a maximum of 10 requests per second per userw
                2,000 requests per hour per IP (or up to a total of 48,000 requests a day)
                
        Response time: around 200 - 400 ms
        
        Yahoo:
            interval : str
            Yahoo:
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo; (Intraday data cannot extend last 60 days)
            Valid count/period:
                1m:             5d
                2m,5m,15m,30m:  1mo
                1h:             <2y
                d1 and above:   10y
            
            Set as default quoter in strategy, fast and stable.
        
        Reference:
        https://github.com/ranaroussi/yfinance
        https://aroussi.com/post/python-yahoo-finance
    """

    def get_1min_bar(self, stock, count='max', extend_trading=False):
        """
        :param stock: str or list
        :param count: number of bars
        :param extend_trading: including before and after trading
        :return: pandas dataframe or dict of dfs
        Same to all other get_bar functions
        """
        if len(stock) == 0:
            logging_error('stock cannot be empty')
            return None

        if type(stock) == str or (type(stock) == list and len(stock) == 1):
            res_df = yf.Ticker(stock).history(period='5d', interval='1m', actions=False, prepost=extend_trading)

            return res_df

        elif type(stock) == list:
            tickers = yf.Tickers(stock)
            df_tickers = tickers.history(period='5d', interval='1m', actions=False,
                                         prepost=extend_trading, group_by="ticker")
            res_dict = {}
            for i in stock:
                res_dict[i] = df_tickers[i]

            return res_dict

    def get_2min_bar(self, stock, count='max', extend_trading=False):
        if len(stock) == 0:
            logging_error('stock cannot be empty')
            return None

        if type(stock) == str or (type(stock) == list and len(stock) == 1):
            res_df = yf.Ticker(stock).history(interval='2m', actions=False, prepost=extend_trading)

            return res_df

        elif type(stock) == list:
            tickers = yf.Tickers(stock)
            df_tickers = tickers.history(interval='2m', actions=False,
                                         prepost=extend_trading, group_by="ticker")
            res_dict = {}
            for i in stock:
                res_dict[i] = df_tickers[i]

            return res_dict

    def get_5min_bar(self, stock, count='max', extend_trading=False):
        if len(stock) == 0:
            logging_error('stock cannot be empty')
            return None

        if type(stock) == str or (type(stock) == list and len(stock) == 1):
            res_df = yf.Ticker(stock).history(interval='5m', actions=False, prepost=extend_trading)

            return res_df

        elif type(stock) == list:
            tickers = yf.Tickers(stock)
            df_tickers = tickers.history(interval='5m', actions=False,
                                         prepost=extend_trading, group_by="ticker")
            res_dict = {}
            for i in stock:
                res_dict[i] = df_tickers[i]

            return res_dict

    def get_15min_bar(self, stock, count='max', extend_trading=False):
        if len(stock) == 0:
            logging_error('stock cannot be empty')
            return None

        if type(stock) == str or (type(stock) == list and len(stock) == 1):
            res_df = yf.Ticker(stock).history(interval='15m', actions=False, prepost=extend_trading)

            return res_df

        elif type(stock) == list:
            tickers = yf.Tickers(stock)
            df_tickers = tickers.history(interval='15m', actions=False,
                                         prepost=extend_trading, group_by="ticker")
            res_dict = {}
            for i in stock:
                res_dict[i] = df_tickers[i]

            return res_dict

    def get_30min_bar(self, stock, count='max', extend_trading=False):
        if len(stock) == 0:
            logging_error('stock cannot be empty')
            return False

        if type(stock) == str or (type(stock) == list and len(stock) == 1):
            res_df = yf.Ticker(stock).history(interval='30m', actions=False, prepost=extend_trading)

            return res_df

        elif type(stock) == list:
            tickers = yf.Tickers(stock)
            df_tickers = tickers.history(interval='30m', actions=False,
                                         prepost=extend_trading, group_by="ticker")
            res_dict = {}
            for i in stock:
                res_dict[i] = df_tickers[i]

            return res_dict

    def get_1h_bar(self, stock, count='max', extend_trading=False):
        if len(stock) == 0:
            logging_error('stock cannot be empty')
            return None
        if count == 'max':
            period = '1y'
        else:
            # specific time period current not working
            pass

        if type(stock) == str or (type(stock) == list and len(stock) == 1):
            res_df = yf.Ticker(stock).history(period=period, interval='1h', actions=False, prepost=extend_trading)

            return res_df

        elif type(stock) == list:
            tickers = yf.Tickers(stock)
            df_tickers = tickers.history(period=period, interval='1h', actions=False,
                                         prepost=extend_trading, group_by="ticker")
            res_dict = {}
            for i in stock:
                res_dict[i] = df_tickers[i]

            return res_dict

    def get_1d_bar(self, stock, count='max', extend_trading=False):
        if len(stock) == 0:
            logging_error('stock cannot be empty')
            return None
        if count == 'max':
            period = '10y'
        else:
            # specific time period current not working, using period instead
            period = count

        if type(stock) == str or (type(stock) == list and len(stock) == 1):
            res_df = yf.Ticker(stock).history(period=period, interval='1d', actions=False, prepost=extend_trading)

            return res_df

        elif type(stock) == list:
            tickers = yf.Tickers(stock)
            df_tickers = tickers.history(period=period, interval='1d', actions=False,
                                         prepost=extend_trading, group_by="ticker")
            res_dict = {}
            for i in stock:
                res_dict[i] = df_tickers[i]

            return res_dict

    def get_1w_bar(self, stock, count='max', extend_trading=False):
        if len(stock) == 0:
            logging_error('stock cannot be empty')
            return None
        if count == 'max':
            period = '10y'
        else:
            # specific time period current not working, using period instead
            period = count

        if type(stock) == str or (type(stock) == list and len(stock) == 1):
            res_df = yf.Ticker(stock).history(period=period, interval='1wk', actions=False, prepost=extend_trading)

            return res_df

        elif type(stock) == list:
            tickers = yf.Tickers(stock)
            df_tickers = tickers.history(period=period, interval='1wk', actions=False,
                                         prepost=extend_trading, group_by="ticker")
            res_dict = {}
            for i in stock:
                res_dict[i] = df_tickers[i]

            return res_dict

