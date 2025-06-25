import pandas as pd 
from events import MarketEvent
import abc 

class DataHandler(abc.ABC):
    @abc.abstractmethod
    def update_bars(self):
        """Read next bar(s) and push MarketEvent(s) onto the queue."""
        raise NotImplementedError()

class HistoricCSVDataHandler(DataHandler):
    def __init__(self, csv_dir, events):
        self.csv_dir         = csv_dir        # Directory containing CSVs
        self.events          = events         # Shared event queue
        self.symbol_data     = {}             # symbol -> iterator over rows
        self.latest_data     = {}             # symbol -> latest price
        self.continue_backtest = True         # Flag to stop when data exhausted

    def _open_csv(self, symbol):
        # Load CSV into DataFrame with datetime index
        df = pd.read_csv(
            f"{self.csv_dir}/{symbol}.csv",
            parse_dates=True,                 # Parse 'datetime' column as timestamps
            index_col='datetime'              # Use 'datetime' as index for time slicing
        )
        self.symbol_data[symbol] = df.iterrows()  # Store iterator for row-by-row reading
        self.latest_data[symbol] = None

    def update_bars(self):
        # Emit one MarketEvent per symbol per call
        any_data = False
        for sym, it in self.symbol_data.items():
            try:
                timestamp, bar = next(it)         # Get the next row
                price = bar['close']              # Use closing price
                self.latest_data[sym] = price     # Keep for mark-to-market
                evt = MarketEvent(timestamp, sym, price)
                self.events.put(evt)              # Push into event queue
                any_data = True
            except StopIteration:
                # No more data for this symbol
                continue
        if not any_data:
            # If no symbol emitted data, end the backtest
            self.continue_backtest = False

    def is_finished(self):
        return not self.continue_backtest

    # (Stub for fetching historical arrays; you'd implement storage for this)
    def get_latest_bars_values(self, symbol, field, N=1):
        raise NotImplementedError("Implement bar history storage")

