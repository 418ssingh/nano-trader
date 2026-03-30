"""
Connection Pool - Manages persistent IBKR connections for low latency
"""

import time
from typing import Optional, List, Dict, Any, Tuple
from contextlib import contextmanager

from ib_async import IB, Stock, Contract, LimitOrder

from .latency_tracker import LatencyTracker, LatencyStats


class ConnectionPool:
    """
    Manages persistent connections to IBKR.
    Eliminates connection handshake overhead for sub-8ms latency.
    
    Usage:
        pool = ConnectionPool()
        pool.connect()
        
        with pool.get_connection() as conn:
            trade = conn.placeOrder(contract, order)
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 4002, pool_size: int = 3):
        self.host = host
        self.port = port
        self.pool_size = pool_size
        
        self._connections: List[IB] = []
        self._current_index = 0
        self._is_connected = False
        
        # Latency trackers
        self.connect_tracker = LatencyTracker(name="Connect")
        self.order_tracker = LatencyTracker(name="Order")
        
    def connect(self) -> None:
        """Create all connections in the pool"""
        print(f"\n🔌 Creating connection pool with {self.pool_size} connections...")
        
        for i in range(self.pool_size):
            start = time.perf_counter_ns()
            
            conn = IB()
            conn.connect(self.host, self.port, clientId=i + 1)
            
            latency_ms = (time.perf_counter_ns() - start) / 1_000_000
            self.connect_tracker.record(latency_ms)
            
            self._connections.append(conn)
            print(f"   Connection {i+1}: {conn.managedAccounts()} ({latency_ms:.2f}ms)")
        
        self._is_connected = True
        print(f"\n✅ Connection pool ready!")
        print(self.connect_tracker.report())
    
    @contextmanager
    def get_connection(self):
        """
        Get a connection from the pool (round-robin).
        Use as context manager for automatic cleanup.
        """
        if not self._is_connected:
            self.connect()
        
        # Round-robin connection selection
        conn = self._connections[self._current_index]
        self._current_index = (self._current_index + 1) % len(self._connections)
        
        try:
            yield conn
        except Exception as e:
            # If connection is dead, reconnect
            if not conn.isConnected():
                print(f"⚠️ Connection lost, reconnecting...")
                conn.connect(self.host, self.port, clientId=self._current_index + 1)
            raise e
    
    def place_limit_order(
        self, 
        symbol: str, 
        quantity: int, 
        price: float,
        action: str = "BUY"
    ) -> Tuple[Any, float]:
        """
        Place a limit order and measure latency.
        
        Returns: (trade_object, latency_ms)
        """
        start_ns = time.perf_counter_ns()
        
        with self.get_connection() as conn:
            # Create and qualify contract
            contract = Stock(symbol, "SMART", "USD")
            qualified = conn.qualifyContracts(contract)
            if qualified:
                contract = qualified[0]
            
            # Place order
            order = LimitOrder(action, quantity, price)
            trade = conn.placeOrder(contract, order)
        
        latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        self.order_tracker.record(latency_ms)
        
        return trade, latency_ms
    
    def cancel_order(self, order_id: int) -> float:
        """Cancel an order and return cancellation latency"""
        start_ns = time.perf_counter_ns()
        
        with self.get_connection() as conn:
            conn.cancelOrder(order_id)
        
        return (time.perf_counter_ns() - start_ns) / 1_000_000
    
    def disconnect(self) -> None:
        """Close all connections"""
        print("\n🔌 Disconnecting all connections...")
        for conn in self._connections:
            if conn.isConnected():
                conn.disconnect()
        self._is_connected = False
        print("✅ All connections closed")
    
    def get_stats(self) -> Dict[str, LatencyStats]:
        """Get all latency statistics"""
        return {
            'connect': self.connect_tracker.stats,
            'order': self.order_tracker.stats
        }
    
    def print_report(self) -> None:
        """Print complete performance report"""
        print("\n" + "=" * 50)
        print("CONNECTION POOL PERFORMANCE REPORT")
        print("=" * 50)
        print(f"Pool Size: {self.pool_size} connections")
        print(f"Connected: {'Yes' if self._is_connected else 'No'}")
        print("\n" + "-" * 50)
        print(self.order_tracker.report())