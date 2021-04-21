import dateutil.parser
import datetime

class Balance:
    def __init__(self, info, exchange):
        if exchange == "binance_futures":
            self.initial_margin = float(info['initialMargin'])
            self.maintenance_margin = float(info['maintMargin'])
            self.margin_balance = float(info['marginBalance'])
            self.wallet_balance = float(info['walletBalance'])
            self.unrealized_pnl = float(info['unrealizedProfit'])

        elif exchange == "binance_spot":
            self.free = float(info['free'])
            self.locked = float(info['locked'])


class Candle:
    def __init__(self, candle_info, timeframe, exchange):
        if exchange in ["binance_futures", "binance_spot"]:
            self.timestamp = candle_info[0]
            self.open = float(candle_info[1])
            self.high = float(candle_info[2])
            self.low = float(candle_info[3])
            self.close = float(candle_info[4])
            self.volume = float(candle_info[5])

        elif exchange == "parse_trade":
            self.timestamp = candle_info['ts']
            self.open = candle_info['open']
            self.high = candle_info['high']
            self.low = candle_info['low']
            self.close = candle_info['close']
            self.volume = candle_info['volume']


def tick_to_decimals(tick_size: float) -> int:
    tick_size_str = "{0:.8f}".format(tick_size)
    while tick_size_str[-1] == "0":
        tick_size_str = tick_size_str[:-1]

    split_tick = tick_size_str.split(".")

    if len(split_tick) > 1:
        return len(split_tick[1])
    else:
        return 0


class Contract:
    def __init__(self, contract_info, exchange):
        if exchange == "binance_futures":
            self.symbol = contract_info['symbol']
            self.base_asset = contract_info['baseAsset']
            self.quote_asset = contract_info['quoteAsset']
            self.price_decimals = contract_info['pricePrecision']
            self.quantity_decimals = contract_info['quantityPrecision']
            self.tick_size = 1 / pow(10, contract_info['pricePrecision'])
            self.lot_size = 1 / pow(10, contract_info['quantityPrecision'])

        elif exchange == "binance_spot":
            self.symbol = contract_info['symbol']
            self.base_asset = contract_info['baseAsset']
            self.quote_asset = contract_info['quoteAsset']

            # The actual lot size and tick size on Binance spot can be found in the 'filters' fields
            # contract_info['filters'] is a list
            for b_filter in contract_info['filters']:
                if b_filter['filterType'] == 'PRICE_FILTER':
                    self.tick_size = float(b_filter['tickSize'])
                    self.price_decimals = tick_to_decimals(float(b_filter['tickSize']))
                if b_filter['filterType'] == 'LOT_SIZE':
                    self.lot_size = float(b_filter['stepSize'])
                    self.quantity_decimals = tick_to_decimals(float(b_filter['stepSize']))

        self.exchange = exchange


class OrderStatus:
    def __init__(self, order_info, exchange):
        if exchange == "binance_futures":
            self.order_id = order_info['orderId']
            self.status = order_info['status'].lower()
            self.avg_price = float(order_info['avgPrice'])
        elif exchange == "binance_spot":
            self.order_id = order_info['orderId']
            self.status = order_info['status'].lower()
            self.avg_price = float(order_info['avgPrice'])


class Trade:
    def __init__(self, trade_info):
        self.time: int = trade_info['time']
        self.contract: Contract = trade_info['contract']
        self.strategy: str = trade_info['strategy']
        self.side: str = trade_info['side']
        self.entry_price: float = trade_info['entry_price']
        self.status: str = trade_info['status']
        self.pnl: float = trade_info['pnl']
        self.quantity = trade_info['quantity']
        self.entry_id = trade_info['entry_id']






