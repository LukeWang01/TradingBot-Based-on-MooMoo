# Dev
# 03/29/2024
# LukeLab for LookAtWallStreet
# Version 1.0
# Programming Trading based on MooMoo API/OpenD

# MooMoo API Documentation, English:
# https://openapi.moomoo.com/moomoo-api-doc/en/intro/intro.html

# 官方文档，中文:
# https://openapi.moomoo.com/moomoo-api-doc/intro/intro.html

from moomoo import *
import schedule

from discord_bot.discord_notify_human import send_msg_to_discord_request
from env._secrete import MooMoo_PWD
from strategy.Your_Strategy import Your_Strategy
from utils.dataIO import get_current_time, print_current_time, logging_info
from utils.time_tool import check_if_weekday, is_market_and_extended_hours

# Environment Variables
MOOMOOOPEND_ADDRESS = "127.0.0.1"  # be same as the OpenD host IP
MOOMOOOPEND_PORT = 11112  # be same as the OpenD port number

TRADING_ENVIRONMENT = TrdEnv.REAL
# REAL = "REAL"
# SIMULATE = "SIMULATE"


TRADING_MARKET = TrdMarket.US       # US market, HK for HongKong, etc.
# NONE = "N/A"  # 未知
# HK = "HK"  # 香港市场
# US = "US"  # 美国市场
# CN = "CN"  # 大陆市场
# HKCC = "HKCC"  # 香港A股通市场
# FUTURES = "FUTURES"  # 期货市场


TRADING_PWD = MooMoo_PWD
# MooMoo_PWD = "your moomoo trading password"


SECURITY_FIRM = SecurityFirm.FUTUINC
# FUTUSECURITIES = 'FUTUSECURITIES'
# FUTUINC = 'FUTUINC'
# FUTUSG = 'FUTUSG'
# FUTUAU = 'FUTUAU'


# Trader class:
class Trader:
    def __init__(self, name='Your Trader Name'):
        self.name = name
        self.trade_context = None

    def init_context(self):
        self.trade_context = OpenSecTradeContext(filter_trdmarket=TRADING_MARKET, host=MOOMOOOPEND_ADDRESS,
                                                 port=MOOMOOOPEND_PORT, security_firm=SECURITY_FIRM)

    def close_context(self):
        self.trade_context.close()

    def unlock_trade(self):
        if TRADING_ENVIRONMENT == TrdEnv.REAL:
            ret, data = self.trade_context.unlock_trade(TRADING_PWD)
            if ret != RET_OK:
                print('Unlock trade failed: ', data)
                return False
            print('Unlock Trade success!')
        return True

    def market_sell(self, stock, quantity, price):
        self.init_context()
        if self.unlock_trade():
            code = f'US.{stock}'
            ret, data = self.trade_context.place_order(price=price, qty=quantity, code=code, trd_side=TrdSide.SELL,
                                                       order_type=OrderType.MARKET, trd_env=TRADING_ENVIRONMENT)
            if ret != RET_OK:
                print('Trader: Market Sell failed: ', data)
                self.close_context()
                return ret, data
            print('Trader: Market Sell success!')
            self.close_context()
            return ret, data
        else:
            data = 'Trader: Market Sell failed: unlock trade failed'
            print(data)
            self.close_context()
            return -1, data

    def market_buy(self, stock, quantity, price):
        self.init_context()
        if self.unlock_trade():
            code = f'US.{stock}'
            ret, data = self.trade_context.place_order(price=price, qty=quantity, code=code, trd_side=TrdSide.BUY,
                                                       order_type=OrderType.MARKET, trd_env=TRADING_ENVIRONMENT)
            if ret != RET_OK:
                print('Trader: Market Buy failed: ', data)
                self.close_context()
                return ret, data
            print('Trader: Market Buy success!')
            self.close_context()
            return ret, data
        else:
            data = 'Trader: Market Buy failed: unlock trade failed'
            print(data)
            self.close_context()
            return -1, data

    def limit_sell(self, stock, quantity, price):
        self.init_context()
        if self.unlock_trade():
            code = f'US.{stock}'
            ret, data = self.trade_context.place_order(price=price, qty=quantity, code=code, trd_side=TrdSide.SELL,
                                                       order_type=OrderType.NORMAL, trd_env=TRADING_ENVIRONMENT,
                                                       fill_outside_rth=True)
            if ret != RET_OK:
                print('Trader: Limit Sell failed: ', data)
                self.close_context()
                return ret, data
            print('Trader: Limit Sell success!')
            self.close_context()
            return ret, data
        else:
            data = 'Trader: Limit Sell failed: unlock trade failed'
            print(data)
            self.close_context()
            return -1, data

    def limit_buy(self, stock, quantity, price):
        self.init_context()
        if self.unlock_trade():
            code = f'US.{stock}'
            ret, data = self.trade_context.place_order(price=price, qty=quantity, code=code, trd_side=TrdSide.BUY,
                                                       order_type=OrderType.NORMAL, trd_env=TRADING_ENVIRONMENT,
                                                       fill_outside_rth=True)
            if ret != RET_OK:
                print('Trader: Limit Buy failed: ', data)
                self.close_context()
                return ret, data
            print('Trader: Limit Buy success!')
            self.close_context()
            return ret, data
        else:
            data = 'Trader: Limit Buy failed: unlock trade failed'
            print(data)
            self.close_context()
            return -1, data

    def get_account_info(self):
        self.init_context()
        if self.unlock_trade():
            ret, data = self.trade_context.accinfo_query()
            if ret != RET_OK:
                print('Trader: Get Account Info failed: ', data)
                self.close_context()
                return ret, data

            acct_info = {
                'cash': round(data["cash"][0], 2),
                'total_assets': round(data["total_assets"][0], 2),
                'market_value': round(data["market_value"][0], 2),
            }
            self.close_context()
            logging_info('Trader: Get Account Info success!')
            return ret, acct_info
        else:
            data = 'Trader: Get Account Info failed: unlock trade failed'
            print(data)
            self.close_context()
            return -1, data

    def get_positions(self):
        # usage: data = trader.get_positions()
        # tqqq_qty = data['TQQQ']['qty']
        # tqqq_market_val = data['TQQQ']['market_val']
        # 'stock_name', 'qty', 'can_sell_qty', 'cost_price', 'cost_price_valid', 'market_val', 'nominal_price',
        # 'pl_ratio', 'pl_ratio_valid', 'pl_val', 'pl_val_valid', 'today_buy_qty', 'today_buy_val', 'today_pl_val',
        # 'today_trd_val', 'today_sell_qty', 'today_sell_val', 'position_side', 'unrealized_pl', 'realized_pl',
        # 'currency', 'trade_unit'
        self.init_context()
        if self.unlock_trade():
            ret, data = self.trade_context.position_list_query()
            if ret != RET_OK:
                print('Trader: Get Positions failed: ', data)
                self.close_context()
                return ret, data
            # refactor the data
            data['code'] = data['code'].str[3:]
            data_dict = data.set_index('code').to_dict(orient='index')
            self.close_context()
            logging_info('Trader: Get Positions success!')
            return ret, data_dict
        else:
            data = 'Trader: Get Positions failed: unlock trade failed'
            print(data)
            self.close_context()
            return -1, data


if __name__ == '__main__':

    print(get_current_time(), 'TradingBOT is running...')
    # Create a trader and strategy object
    trader = Trader()
    strategy = Your_Strategy(trader)
    print("trader and strategy objects created...")

    # schedule the task
    bot_task = schedule.Scheduler()
    bot_task.every().minute.at(":05").do(strategy.strategy_decision)

    # print the time every hour showing bot running...
    bkg_task = schedule.Scheduler()
    bkg_task.every().hour.at(":00").do(print_current_time)

    print("schedule the task...")

    # loop and keep the schedule running
    while True:
        bkg_task.run_pending()
        if is_market_and_extended_hours() and check_if_weekday():
            try:
                bot_task.run_pending()
            except Exception as e:
                print(get_current_time(), 'Error in the strategy loop:', e)
                # uncomment the code below to send error message to discord
                # send_msg_to_discord_request(f"Bot Error, Fix ASAP: {e}", channel_id=channel_id_dev_bot)
                time.sleep(1)
                continue
        time.sleep(1)
