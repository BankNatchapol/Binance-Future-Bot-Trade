import tkinter as tk
import logging
import pprint

from binance_futures import BinanceFuturesClient
from SECRET import *

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
    
    binance_client = BinanceFuturesClient(PUBLIC_KEY, SECRET_KEY, True)



    calibri_font = ("Calibri", 11, "normal")

    root = tk.Tk()



    root.mainloop()

