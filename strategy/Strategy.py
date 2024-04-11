from discord_bot.discord_notify_human import send_msg_to_discord_request
from quoter.quoter_Webull import Quoter_Webull
from quoter.quoter_Yahoo import Quoter_Yahoo
from utils.dataIO import get_current_time, logging_info
# from utils.send_email import send_emails


class Strategy:
    """
    Class Name must be the same as the file name
    """

    def __init__(self, quoter="yahoo"):
        # define your own strategy name, and indicator
        self.strategy_name = "strategy template class"
        self.strategy_actions_history = "strategy_actions_history"
        self.parent = None  # parent is the main program, app.py

        # set market data quoter
        # default is yh_quoter, fast and stable
        self.quoter = None
        if quoter == "yahoo":
            self.quoter = Quoter_Yahoo()
        elif quoter == "webull":
            self.quoter = Quoter_Webull()

        # self.cash_balance = 0
        # self.market_value = 0
        # self.dayBuyingPower = 0
        # self.overnightBuyingPower = 0
        # self.net_account_value = 0

        # schedule the strategy to run
        # self.strategy_scheduler()
        self.strategy_load_notification()

    """
    Response time: 
        wb_quoter:  around 300 - 800 ms
        yh_quoter:  around 50 - 400 ms (fairly stable)
        
    Intraday (exclude pre-market and after-market):
    < 15 min:   yh_quoter will get more data
    > 15 min:   Quoter_Webull will get more data
    = 1h:       yh_quoter will get more data
    >= 1d:      yh_quoter will get more data
    
    Intraday (include pre-market and after-market):
    < 15 min:   yh_quoter will get more data
    > 15 min:   yh_quoter will get more data
    = 1h:       yh_quoter will get more data
    >= 1d:      yh_quoter will get more data
    
    """

    # ******
    # Functions below need to overwrite in your own strategy class
    def strategy_decision(self):
        pass

    # ******
    # Functions below do not need to be modified, free to check and call
    def strategy_load_notification(self):
        print(f"{self.strategy_name}: Strategy Loaded and Running")
        pass

    # def save_strategy_actions(self, action_res):
    #     if action_res:
    #         write_trading_log_json("trading_actions.json", action_res)

    def update_strategy_profile(self):
        # after placing order, update the strategy profile
        # you can define attributes depends on your strategy
        pass

    def send_notification_via_email(self, msg_body):
        pass

    def send_notification_via_discord(self, msg_body, your_channel_id):
        msg = '```\n'
        msg += f'{get_current_time()}\n'
        msg += msg_body
        msg += '```\n'
        send_msg_to_discord_request(msg, channel_id=your_channel_id)
        logging_info(f"Strategy: {self.strategy_name} Status: Discord msg sent")

    def get_current_position(self):
        pass

    def check_1m_bar(self, stock):
        if self.quoter:
            return self.quoter.get_1min_bar(
                stock=stock, count="max", extend_trading=False
            )

    def check_2m_bar(self, stock):
        if self.quoter:
            return self.quoter.get_2min_bar(
                stock=stock, count="max", extend_trading=False
            )

    def check_5m_bar(self, stock):
        if self.quoter:
            return self.quoter.get_5min_bar(
                stock=stock, count="max", extend_trading=False
            )

    def check_15m_bar(self, stock):
        if self.quoter:
            return self.quoter.get_15min_bar(
                stock=stock, count="max", extend_trading=False
            )

    def check_30m_bar(self, stock):
        if self.quoter:
            return self.quoter.get_30min_bar(
                stock=stock, count="max", extend_trading=False
            )

    def check_1h_bar(self, stock):
        if self.quoter:
            return self.quoter.get_1h_bar(stock=stock, count="1y", extend_trading=False)

    def check_1d_bar(self, stock):
        if self.quoter:
            return self.quoter.get_1d_bar(stock=stock, count="1y", extend_trading=False)

    def check_1w_bar(self, stock):
        if self.quoter:
            return self.quoter.get_1w_bar(stock=stock, count="1y", extend_trading=False)
