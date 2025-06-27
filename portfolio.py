from events import OrderEvent

class Portfolio:
    def __init__(self, start_cash=100_000, base_notional=10_000):
        self.cash         = start_cash
        self.base_notional = base_notional  # dollars per leg at weight=1.0
        self.positions    = {}
        self.holdings     = []

    def generate_order(self, signal, last_price):
        # desired dollar exposure = base_notional * weight
        target_notional = self.base_notional * signal.weight

        # quantity = notional / price, rounded to an integer
        qty = int(target_notional / last_price)

        # for EXIT signals, flip the sign to unwind
        if signal.signal_type == 'EXIT':
            qty = -self.positions.get(signal.symbol, 0)

        # LONG vs SHORT
        direction = 1 if signal.signal_type == 'LONG' else -1
        return OrderEvent(signal.symbol, 'MKT', direction * abs(qty))
