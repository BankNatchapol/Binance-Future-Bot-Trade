import tkinter as tk
import logging
import pprint
from binance_futures import BinanceFuturesClient

logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("info.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# logger.debug("Using for debugging program.")
# logger.info("Using for show basic information.")
# logger.warning("Using for show something you should pay attention.")
# logger.error("Using for helping debug error.")

if __name__ == "__main__":
    
    client = BinanceFuturesClient(True)
    binance_future_contracts = client.get_bid_ask("BTCUSDT")

    calibri_font = ("Calibri", 11, "normal")

    root = tk.Tk()
    root.configure(bg = "gray12")

    pprint.pprint(binance_future_contracts)
    # r = 0
    # c = 0
    # for contract in binance_future_contracts:
    #     label_widget = tk.Label(root, text = contract,
    #                             bg = "gray12",
    #                             fg = "SteelBlue1", 
    #                             borderwidth = 1, 
    #                             relief = tk.SOLID, 
    #                             width = 13, 
    #                             font=calibri_font)
    #     label_widget.grid(row = r, column = c, sticky = "ew")
    #     if r == 16:
    #         c += 1
    #         r = 0
    #     else: 
    #         r += 1

    root.mainloop()


