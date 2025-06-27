from collections import deque
import numpy as np
from events import SignalEvent

class PairsTrading:
    def __init__(self, symbol_x, symbol_y, lookback=60, entry_z=2.0, exit_z=0.5):
        self.symbol_x= symbol_x
        self.symbol_y= symbol_y
        self.lookback= lookback
        self.entry_z= entry_z
        self.exit_z= exit_z
        self.histx= deque(maxlen= lookback) #queue of length lookbcack whioch update when new information comes
        self.histy= deque(maxlen= lookback)
        self.in_position = False
    
    def calculate_signal(self, symbol, price, timestamp):

        #1) Update history for symbol just ticked
        if symbol == self.symbol_y:
            self.histy.append(price)
        elif symbol == self.symbol_x:
            self.histx.append(price)
        else:
            return []  # ignore other symbols
        
        # 2) Wait until both histories are full
        if len(self.histy) < self.lookback or len(self.histx) < self.lookback:
            return []
        
        # 3) Prepare arrays for regression
        y= np.array(self.histy)
        x= np.array(self.histx)
        #4)fit regression
        beta, alpha = np.polyfit(x,y,1)

        #5) Compute current spread and its z-score
        spread    = y[-1] - (beta * x[-1] + alpha)
        spreads   = y - (beta * x + alpha)
        mean, std = spreads.mean(), spreads.std(ddof=1)
        zscore    = (spread - mean) / std

        signals = []
        if not self.in_position:
             signals = []

        # 5) Entry logic
        if not self.in_position:
            if zscore > self.entry_z: 
                # spread is high (latest spread is 2 standard deviation bigger than mean spead) → SHORT y, LONG x (we bet on mean reversion)
                signals.append(SignalEvent(self.symbol_y, timestamp, 'SHORT', 1.0))
                signals.append(SignalEvent(self.symbol_x, timestamp, 'LONG', 1.0))
                self.in_position = True
            elif zscore < -self.entry_z:
                # spread is low → LONG y, SHORT x
                signals.append(SignalEvent(self.symbol_y, timestamp, 'LONG', 1.0))
                signals.append(SignalEvent(self.symbol_x, timestamp, 'SHORT', 1.0))
                self.in_position = True

        # 6) Exit logic
        else:
            if abs(zscore) < self.exit_z:
                # close both legs
                signals.append(SignalEvent(self.symbol_y, timestamp, 'EXIT', 1.0))
                signals.append(SignalEvent(self.symbol_x, timestamp, 'EXIT', 1.0))
                self.in_position = False

        return signals


    
