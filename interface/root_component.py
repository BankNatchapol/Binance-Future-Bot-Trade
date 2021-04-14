import tkinter as tk
import time 

from interface.styling import *
from interface.logging_component import Logging

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trading Bot")

        self.configure(bg = BG_COLOR)

        self.left_frame = tk.Frame(self, bg = BG_COLOR)
        self.left_frame.pack(side = tk.LEFT)
        
        self.right_frame = tk.Frame(self, bg = BG_COLOR)
        self.right_frame.pack(side = tk.RIGHT)

        self._logging_frame = Logging(self.left_frame, bg = BG_COLOR)
        self._logging_frame.pack(side = tk.TOP)

        self._logging_frame.add_log("This is test message.")
        time.sleep(2)
        self._logging_frame.add_log("This is another test message.")