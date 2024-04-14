"""
By: LukeLab
Created on 09/20/2023
Version: 1.0
Last Modified: 09/27/2023

Major Updated: 04/04/2024, decision and order function furnish
Still in testing

updated: 04/09/2024, output formatting

The most basic core trading data and its strategy:
Price and volume

Abstract:
Long-only, swing trading strategy, using RSI indicator to determine the entry and exit point, using probability and
portfolio management to determine the position size and risk management.
"""
import time

# import talib
import yfinance as yf
from moomoo import *

# from TradingBOT import BOT_MAX_TRADING_LIMIT, ACCOUNT_CASH_THRESHOLD
# from discord_bot.discord_notify_bot import run_bot_send_msg_new_thread
from env._secrete import your_channel_id
from strategy.Strategy import Strategy
import pandas_ta as pta
from utils import play_sound
from utils.dataIO import read_json_file, write_json_file, get_current_time, logging_info


class Your_Strategy(Strategy):
    """
    Class Name must be the same as the file name
    """

    def __init__(self, trader):
        super().__init__()
        self.strategy_name = "Type your strategy name here"
        self.trader = trader

        """⬇️⬇️⬇️ Strategy Settings ⬇️⬇️⬇️"""

        self.stock_tracking_list = ["SOXL", "TQQQ", "BITO"]
        self.stock_trading_list = ["SOXL", "TQQQ"]

        # self.cash_balance = 0
        self.strategy_market_value = 0
        self.strategy_market_limit = 9999
        self.strategy_cash_threshold = 9999

        """⬆️⬆️⬆️ Strategy Settings ⬆️⬆️⬆️"""

        self.strategy_position = {}
        self.init_strategy_position()

        print(f"Strategy {self.strategy_name} initialized...")

    """ 
    You only need to define the strategy_decision() function below, and click run strategy button on the App.
    Other functions are defined in the parent class, Strategy.py, you can use them directly.
    Define your own strategy here:
    """

    def strategy_decision(self):
        print("Strategy Decision running...")

        """A Simple Example Strategy from chatGPT"""
        # Strategy starts here

        for stock in self.stock_tracking_list:

            # 1. get the stock data from quoter, return a pandas dataframe
            data = yf.Ticker(stock).history(interval="1h", actions=False, prepost=False, raise_errors=True)

            # 2. calculate the indicator
            data['RSI'] = pta.rsi(data['Close'], length=14)

            pre_rsi = data['RSI'][-2]
            qty = 99
            price = data['Close'][-1]

            # 3. check the strategy condition,
            # For this example, simply buy when rsi < 30, sell when rsi > 70
            if pre_rsi < 30:
                print('buy point start')
                ret, data = self.trader.limit_buy(stock, qty, price)
                if ret == RET_OK:
                    # order placed successfully:
                    self.save_trading_status('BUY', stock, price, 'strategy_decision')
                    self.save_order_history(data, 'strategy_decision')
                    self.update_strategy_position('success', stock, price, qty, 'BUY')
                    play_sound.order_placed()
                else:
                    # order failed
                    print(f"{get_current_time()}: place_order error, {data}")
                    logging_info(f'place_order error, {data}')
                    # self.send_notification_via_discord(data, channel_id_dev_bot)

            elif pre_rsi > 70:
                print('sell point start')
                ret, data = self.trader.limit_sell(stock, qty, price)
                if ret == RET_OK:
                    # order placed successfully:
                    self.save_trading_status('SELL', stock, price, 'strategy_decision')
                    self.save_order_history(data, 'strategy_decision')
                    self.update_strategy_position('success', stock, price, qty, 'SELL')
                    play_sound.order_placed()
                else:
                    print(f"{get_current_time()}: place_order error, {data}")
                    logging_info(f'place_order error, {data}')
                    # self.send_notification_via_discord(data, channel_id_dev_bot)

            # Strategy ends here
            """A Simple Example Strategy from chatGPT"""

            time.sleep(1)  # sleep 1 second to avoid the quote limit

        print("Strategy checked... Waiting next decision called...")
        print('-----------------------------------------------')

    """ ⬇️⬇️⬇️ Order and notification related functions ⬇️⬇️⬇️"""

    def init_strategy_position(self):
        position = read_json_file("strategy_position.json")
        if position:
            # stock_scope = [stock['name'] for stock in position]
            self.strategy_position = position
            for stock in self.stock_trading_list:
                self.strategy_market_value += self.strategy_position[stock]["market_value"]
        else:
            for stock in self.stock_tracking_list:
                self.strategy_position[stock] = {
                    "ticker": stock,
                    "quantity": 0,
                    "market_value": 0,
                    "price": 0,
                    "avg_price": 0,
                    "total_cost": 0,
                    "profit": 0,
                    "profit_percent": 0,
                }
            write_json_file("strategy_position.json", self.strategy_position)

    def save_trading_status(self, order_direction, stock, order_price, called_by):
        logging_info(f'{get_current_time()}: {order_direction}, {stock} @ ${order_price}, {called_by} \n')
        # send the message to Discord channel
        msg_body = ""
        msg_body += f"{order_direction}, {stock} @ ${order_price} \n"
        print(msg_body)
        # uncomment the code below if you need to send the notification to Discord
        # self.send_notification_via_discord(msg_body, your_channel_id)

    def save_order_history(self, data, called_by):
        file_data = read_json_file("order_history.json")
        data_dict = data.to_dict()
        new_dict = {}
        for key, v in data_dict.items():
            new_dict[key] = v[0]
        new_dict['called_by'] = called_by
        logging_info(f'{self.strategy_name}: {str(new_dict)}')

        if file_data:
            file_data.append(new_dict)
        else:
            file_data = [new_dict]
        write_json_file("order_history.json", file_data)

    def update_strategy_position(self, action_res, stock, price, qty, order_direction):
        if action_res == "success":
            # stock = action_res["stock"]
            price = float(price)
            qty = int(qty)
            crt_order_value = round(price * qty, 2)
            # order_direction = action_res["order_direction"]
            if order_direction == "BUY":
                self.strategy_position[stock]["quantity"] += qty
                self.strategy_position[stock]["price"] = price
                self.strategy_position[stock]["market_value"] = round(self.strategy_position[stock]["quantity"] * price,
                                                                      2)
                self.strategy_position[stock]["total_cost"] += crt_order_value
                self.strategy_position[stock]["avg_price"] = round(
                    self.strategy_position[stock]["total_cost"] / self.strategy_position[stock]["quantity"], 2)

                self.strategy_position[stock]["profit"] = round(self.strategy_position[stock]["market_value"] - self.strategy_position[stock]["total_cost"], 2)

                self.strategy_position[stock]["profit_percent"] = round(
                    self.strategy_position[stock]["profit"] / self.strategy_position[stock]["total_cost"], 2)
                self.strategy_market_value += crt_order_value

            elif order_direction == "SELL":
                self.strategy_position[stock]["quantity"] -= qty
                self.strategy_position[stock]["price"] = price
                self.strategy_position[stock]["market_value"] = round(self.strategy_position[stock]["quantity"] * price,
                                                                      2)
                self.strategy_position[stock]["total_cost"] -= crt_order_value
                # self.strategy_position[stock]["avg_price"] = self.strategy_position[stock]["total_cost"] / self.strategy_position[stock]["quantity"]
                # in this method, no change for the avg price when sell
                self.strategy_position[stock]["profit"] = round(self.strategy_position[stock]["market_value"] - self.strategy_position[stock]["total_cost"], 2)

                self.strategy_position[stock]["profit_percent"] = round(
                    self.strategy_position[stock]["profit"] / self.strategy_position[stock]["total_cost"], 2)
                self.strategy_market_value -= crt_order_value
            else:
                print("wrong order direction")

            write_json_file("strategy_position.json", self.strategy_position)
