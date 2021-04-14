import tkinter as tk
import time 

from connectors.binance_futures import BinanceFuturesClient

from interface.styling import *
from interface.logging_component import Logging
from interface.watchlist_component import WatchList

import logging

logger = logging.getLogger()

class Root(tk.Tk):
    def __init__(self, binance_f: BinanceFuturesClient):
        super().__init__()

        self.binance_f = binance_f

        self.title("Trading Bot")

        self.configure(bg = BG_COLOR)

        self._left_frame = tk.Frame(self, bg = BG_COLOR)
        self._left_frame.pack(side = tk.LEFT)
        
        self._right_frame = tk.Frame(self, bg = BG_COLOR)
        self._right_frame.pack(side = tk.RIGHT)

        self._watchlist_frame = WatchList(self.binance_f.contracts, self._left_frame, bg = BG_COLOR)
        self._watchlist_frame.pack(side = tk.TOP)

        self._logging_frame = Logging(self._left_frame, bg = BG_COLOR)
        self._logging_frame.pack(side = tk.TOP)

        self._update_ui()

    def _update_ui(self):
        for log in self.binance_f.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True
        try:
            for key, value in self._watchlist_frame.body_widgets['symbol'].items():
                symbol = self._watchlist_frame.body_widgets['symbol'][key].cget("text")
                exchange = self._watchlist_frame.body_widgets['exchange'][key].cget("text")

                if exchange == "Binance Futures":
                    if symbol not in self.binance_f.contracts:
                        continue

                    if symbol not in self.binance_f.prices:
                        self.binance_f.get_bid_ask(self.binance_f.contracts[symbol])
                        continue
                    
                    precision = self.binance_f.contracts[symbol].price_decimals
                    prices = self.binance_f.prices[symbol]
                else:
                    continue

                if prices['bid'] is not None:
                    price_str = "{0:.{prec}f}".format(prices['bid'], prec = precision)
                    self._watchlist_frame.body_widgets['bid_var'][key].set(price_str)
                if prices['ask'] is not None:
                    price_str = "{0:.{prec}f}".format(prices['ask'], prec = precision)
                    self._watchlist_frame.body_widgets['ask_var'][key].set(price_str)
        except RuntimeError as e:
            logger.error("Error while lopping through watchlist dictionary: %s", e)

        self.after(1500, self._update_ui)