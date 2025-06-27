from enum import Enum

# Define all event types our engine has to handle
class EventType(Enum):
    Market = "MARKET"   # New Market data
    Signal = "SIGNAL"   # Our strategy wants to enter or exit trade
    ORDER  = "ORDER"    # Order has been sent to the market
    FILL   = "FILL"     # Actual trade execution with fees/slippage

# Base Event class
class Event:
    def __init__(self, type):
        self.type = type  # For example: EventType.Market

# Event emitted when new market data is available
class MarketEvent(Event):
    def __init__(self, timestamp, symbol, price):
        super().__init__(EventType.Market)
        self.timestamp = timestamp
        self.symbol    = symbol
        self.price     = price

# Event emitted by strategy to signal trade intention
class SignalEvent(Event):
    def __init__(self, symbol, datetime, signal_type, weight):
        super().__init__(EventType.Signal)
        self.symbol      = symbol
        self.datetime    = datetime
        self.signal_type = signal_type  # 'LONG', 'SHORT', or 'EXIT'
        self.weight      = weight       # e.g., 1.0 = full position

# Optional: OrderEvent if you're using a Portfolio with order simulation
class OrderEvent(Event):
    def __init__(self, symbol, order_type, quantity):
        super().__init__(EventType.ORDER)
        self.symbol     = symbol
        self.order_type = order_type  # Usually 'MKT' for market
        self.quantity   = quantity
