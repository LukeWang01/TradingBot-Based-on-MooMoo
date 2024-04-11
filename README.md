# TradingBot Based on MooMoo/Futu
<br>
Note: Don't share any API key, secret key, or password.
<br>
Install requirements: run in cmd under root directory: `pip install -r requirements.txt`

Install MooMoo/Futu OpenD: https://www.moomoo.com/download/OpenAPI
Office Docs for OpenD: https://openapi.moomoo.com/moomoo-api-doc/en/quick/opend-base.html

Recommended to open with PyCharm, download and install: https://www.jetbrains.com/products/compare/?product=pycharm&product=pycharm-ce

<br>

#### Easy for Four Steps:

1. Go to the `env/_secret.py` and fill in your trading password and Discord info.
2. Go to the `strategy/Your_Strategy.py`, and replace the example strategy in `strategy_decision(self)` with your own strategy
3. Login to MooMoo/Futu OpenD, setup the port number to 11112 or 11111, which should be the same as `MOOMOOOPEND_PORT` in `TradingBOT.py`.
4. Go to the project root directory and run `python TradingBOT.py` 
5. Any questions, please contact me: `Discord/Wechat: squawkwallstreet`.