import tkinter as tk
from tkinter.messagebox import askquestion

import time 
import json

from connectors.binance import BinanceClient

from interface.styling import *
from interface.logging_component import Logging
from interface.watchlist_component import WatchList
from interface.trades_component import TradesWatch
from interface.strategy_component import StrategyEditor

import logging

logger = logging.getLogger()

class Root(tk.Tk):
    def __init__(self, binance: BinanceClient):
        super().__init__()

        self.binance = binance

        self.title("Trading Bot")
        self.protocol("WM_DELETE_WINDOW", self._ask_before_close)

        self.configure(bg = BG_COLOR)
        
        self.main_menu = tk.Menu(self)
        self.configure(menu = self.main_menu)

        self.workspace_menu = tk.Menu(self.main_menu, tearoff = False)
        self.main_menu.add_cascade(label = "Workspace", menu = self.workspace_menu)
        self.workspace_menu.add_command(label = "Save workspace", command = self._save_workspace)

        self._left_frame = tk.Frame(self, bg = BG_COLOR)
        self._left_frame.pack(side = tk.LEFT)
        
        self._right_frame = tk.Frame(self, bg = BG_COLOR)
        self._right_frame.pack(side = tk.RIGHT)

        self._watchlist_frame = WatchList(self.binance.contracts, self._left_frame, bg = BG_COLOR)
        self._watchlist_frame.pack(side = tk.TOP)

        self.logging_frame = Logging(self._left_frame, bg = BG_COLOR)
        self.logging_frame.pack(side = tk.TOP)

        self._strategy_frame = StrategyEditor(self, self.binance, self._right_frame, bg = BG_COLOR)
        self._strategy_frame.pack(side = tk.TOP)

        self._trades_frame = TradesWatch(self._right_frame, bg = BG_COLOR)
        self._trades_frame.pack(side = tk.TOP)

        self._update_ui()

    def _ask_before_close(self):
        result = askquestion("Confirmation", "Do you want to exit the application?")
        if result == "yes":
            self.binance.reconnect = False
            self.binance.ws.close()

            self.destroy()

    def _update_ui(self):
        for log in self.binance.logs:
            if not log['displayed']:
                self.logging_frame.add_log(log['log'])
                log['displayed'] = True

        for client in [self.binance]:
            try: 
                for b_index, strat in client.strategies.items():
                    for log in strat.logs:
                        self.logging_frame.add_log(log['log'])
                        log['displayed'] = True
                    for trade in strat.trades:
                        if trade.time not in self._trades_frame.body_widgets['symbol']:
                            self._trades_frame.add_trade(trade)
                        
                        if trade.contract.exchange == "Binance":
                            precision = trade.contract.price_decimals 
                        else:
                            precision = 8
                        
                        
                        pnl_str = "{0:.{prec}f}".format(trade.pnl, prec = precision)
                        self._trades_frame.body_widgets['pnl_var'][trade.time].set(pnl_str)
                        self._trades_frame.body_widgets['status_var'][trade.time].set(trade.status.capitalize())

            except RuntimeError as e:
                logger.error("Error while lopping through strategies dictionary: %s", e)
        try:
            for key, value in self._watchlist_frame.body_widgets['symbol'].items():
                symbol = self._watchlist_frame.body_widgets['symbol'][key].cget("text")
                exchange = self._watchlist_frame.body_widgets['exchange'][key].cget("text")

                if exchange == "Binance":
                    if symbol not in self.binance.contracts:
                        continue

                    if symbol not in self.binance.prices:
                        self.binance.get_bid_ask(self.binance.contracts[symbol])
                        continue
                    
                    precision = self.binance.contracts[symbol].price_decimals
                    prices = self.binance.prices[symbol]
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

    def _save_workspace(self):

        """
        Collect the current data on the interface and saves it to the SQLite database to avoid setting up everything
        again everytime you open the program.
        Triggered from a Menu command.
        :return:
        """

        # Watchlist

        watchlist_symbols = []

        for key, value in self._watchlist_frame.body_widgets['symbol'].items():
            symbol = value.cget("text")
            exchange = self._watchlist_frame.body_widgets['exchange'][key].cget("text")

            watchlist_symbols.append((symbol, exchange,))

        self._watchlist_frame.db.save("watchlist", watchlist_symbols)

        # Strategies

        strategies = []

        strat_widgets = self._strategy_frame.body_widgets

        for b_index in strat_widgets['contract']:  # Loops through the rows of a column (not necessarily the 'contract' one

            strategy_type = strat_widgets['strategy_type_var'][b_index].get()
            contract = strat_widgets['contract_var'][b_index].get()
            timeframe = strat_widgets['timeframe_var'][b_index].get()
            balance_pct = strat_widgets['balance_pct'][b_index].get()
            take_profit = strat_widgets['take_profit'][b_index].get()
            stop_loss = strat_widgets['stop_loss'][b_index].get()

            # Extra parameters are all saved in one column as a JSON string because they change based on the strategy

            extra_params = dict()

            for param in self._strategy_frame.extra_params[strategy_type]:
                code_name = param['code_name']

                extra_params[code_name] = self._strategy_frame.additional_parameters[b_index][code_name]

            strategies.append((strategy_type, contract, timeframe, balance_pct, take_profit, stop_loss,
                               json.dumps(extra_params),))

        self._strategy_frame.db.save("strategies", strategies)

        self.logging_frame.add_log("Workspace saved")