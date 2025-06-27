import enum as Enum

#Define all events types our engine has to handle
class EventType(Enum):
    Market="MARKET" # New Market data
    Signal="SIGNAL" # Our Strategy wants to enter or exit trade
    ORDER  = "ORDER" # ORDER is executed in market
    FILL   = "FILL" # Actual trade execution with all microstructure noises (fees, taxes) added to update portfolio


# Base Event class, carries only the event type.
class Event:                  
    def __init__(self, type):
        self.type= type         # ex: Create an Event instance: evt = Event(EventType.MARKET) then we can call evt.type

# Event emitted when new market row price data is ready.
class MarketEvent(Event):
    def __init__(self, timestamp, symbol, price):
        super().__init__(EventType.Market) #tag as market event
        self.timestamp= timestamp
        self.symbol= symbol
        self.price= price
        
class OrderEvent(Event):
    def __init__(self, symbol, quantity):
        super().__init__(EventType.ORDER)
        self.symbol = symbol
        self.quantity = quantity

# Event emitted by the strategy indicating a buy/sell/exit.
class SignalEvent(Event):
    def __init__(self, symbol, datetime, signal_type, weight):
        super().__init__(EventType.Signal) #tag as signal event
        self.symbol= symbol                #symbol the signal is for
        self.datetime= datetime            #Time of signal generation
        self.signal_type= signal_type      #Long, short or exit
        self.weight= weight                #sizing of signal


        



