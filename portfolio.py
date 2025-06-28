from events import OrderEvent

class Portfolio:
    def __init__(self, start_cash=100_000, base_notional=10_000):
        self.cash          = start_cash
        self.base_notional = base_notional
        self.positions     = {}      # symbol → quantity
        self.holdings      = []      # list of (date, NAV)

    def generate_order(self, signal, last_price):
        target_notional = self.base_notional * signal.weight
        qty = int(target_notional / last_price)

        if signal.signal_type == 'EXIT':
            qty = -self.positions.get(signal.symbol, 0)

        direction = 1 if signal.signal_type == 'LONG' else -1
        qty *= direction

        # Update cash and position (basic fill logic)
        trade_cost = qty * last_price
        self.cash -= trade_cost
        self.positions[signal.symbol] = self.positions.get(signal.symbol, 0) + qty

        return OrderEvent(signal.symbol, 'MKT', qty)

    def update_timeindex(self, date, last_prices):
        # Recalculate portfolio NAV
        nav = self.cash
        for sym, qty in self.positions.items():
            nav += qty * last_prices.get(sym, 0)

        # Append date + NAV for performance tracking
        self.holdings.append((date, nav))
