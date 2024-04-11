from webull import webull

from quoter.Quoter import Quoter
from utils.dataIO import logging_info, logging_error, logging_warning


class Quoter_Webull(Quoter):

    def __init__(self):
        super().__init__()
        self.name = "Webull Platform"
        self.wb = webull()
        logging_info('Quoter_Webull created')

    """
        response time: around 400 - 800 ms
        Webull:
                Valid intervals: m1, m5, m15, m30, d1;  (h1, h2, h4, w1 are currently not working)
                max_count:
                    m1:     1200
                    m5:     1200
                    m15:    1200
                    m30:    1049
                    d1:     1200
                interval : str
                return: pandas dataframe
    """

    def get_current_quote(self, stock):
        # best to call in Trader class
        try:
            response = self.wb.get_quote(stock)
            ask_price_1 = response['askList'][0]['price']
            bid_price_1 = response['bidList'][0]['price']
            res = (bid_price_1, ask_price_1)
            logging_info('Get current quote')
            return res
        except KeyError:
            logging_error('Please login to get the real time quote')
            return None

    def get_1min_bar(self, stock, count='max', extend_trading=False):
        # TODO: need to check if the count is valid, same for others
        cnt = 1200 if count == 'max' else count
        extend = 1 if extend_trading else 0
        response = self.wb.get_bars(stock, interval='m1', count=cnt, extendTrading=extend)
        if len(response) == cnt and len(response) == 1:
            return response
        else:
            logging_warning('Quote count exceed server max count')
            return None

    def get_5min_bar(self, stock, count='max', extend_trading=False):
        cnt = 1200 if count == 'max' else count
        extend = 1 if extend_trading else 0
        response = self.wb.get_bars(stock, interval='m5', count=cnt, extendTrading=extend)
        if not len(response) == cnt and len(response) == 1:
            response = None
            logging_warning('Quote count exceed server max count')
        return response

    def get_15min_bar(self, stock, count='max', extend_trading=False):
        cnt = 1200 if count == 'max' else count
        extend = 1 if extend_trading else 0
        response = self.wb.get_bars(stock, interval='m15', count=cnt, extendTrading=extend)
        if not len(response) == cnt and len(response) == 1:
            response = None
            logging_warning('Quote count exceed server max count')
        return response

    def get_30min_bar(self, stock, count='max', extend_trading=False):
        cnt = 1049 if count == 'max' else count
        extend = 1 if extend_trading else 0
        response = self.wb.get_bars(stock, interval='m30', count=cnt, extendTrading=extend)
        if not len(response) == cnt and len(response) == 1:
            response = None
            logging_warning('Quote count exceed server max count')
        return response

    def get_1d_bar(self, stock, count='max', extend_trading=False):
        cnt = 1200 if count == 'max' else count
        extend = 1 if extend_trading else 0
        response = self.wb.get_bars(stock, interval='d1', count=cnt, extendTrading=extend)
        if not len(response) == cnt and len(response) == 1:
            response = None
            logging_warning('Quote count exceed server max count')
        return response

    def get_1w_bar(self, stock, count='max', extend_trading=False):
        cnt = 1200 if count == 'max' else count
        extend = 1 if extend_trading else 0
        response = self.wb.get_bars(stock, interval='w1', count=cnt, extendTrading=extend)
        if not len(response) == cnt and len(response) == 1:
            response = None
            logging_warning('Quote count exceed server max count')
        return response
