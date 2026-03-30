"""
Simple test for Connection Pool - No orders, just connection and latency
"""

import time
from nano_trader.core.connection_pool import ConnectionPool


def test_pool_connections():
    """Test just the connection pool without orders"""
    print("\n" + "=" * 60)
    print("TESTING CONNECTION POOL (No Orders)")
    print("=" * 60)
    
    # Create pool
    pool = ConnectionPool(host="127.0.0.1", port=4002, pool_size=3)
    
    # Connect only (no orders)
    pool.connect()
    
    # Test round-robin connection access
    print("\n📝 Testing connection access (round-robin)...")
    
    for i in range(6):
        with pool.get_connection() as conn:
            accounts = conn.managedAccounts()
            print(f"   Access {i+1}: Connection {pool._current_index}, Account: {accounts}")
        time.sleep(0.1)
    
    # Show connection stats
    print("\n📊 Connection Pool Stats:")
    print(f"   Total connections: {pool.pool_size}")
    print(f"   Connection latency: {pool.connect_tracker.stats.avg_ms:.2f}ms avg")
    
    pool.disconnect()
    
    print("\n✅ Connection pool test completed!")
    return pool


def test_order_without_pool():
    """Test direct order placement without pool for baseline"""
    print("\n" + "=" * 60)
    print("TESTING DIRECT ORDER (No Pool)")
    print("=" * 60)
    
    from ib_async import IB, Stock, LimitOrder
    
    ib = IB()
    ib.connect('127.0.0.1', 4002, clientId=99)
    
    # Qualify contract
    contract = Stock('AAPL', 'SMART', 'USD')
    qualified = ib.qualifyContracts(contract)
    if qualified:
        contract = qualified[0]
    
    # Test order latency
    latencies = []
    order_ids = []
    
    print("\n📝 Placing 5 test orders...")
    
    for i in range(5):
        order = LimitOrder("BUY", 1, 150.00)  # Realistic price
        
        start = time.perf_counter_ns()
        trade = ib.placeOrder(contract, order)
        end = time.perf_counter_ns()
        
        latency_ms = (end - start) / 1_000_000
        latencies.append(latency_ms)
        
        if hasattr(trade, 'order') and hasattr(trade.order, 'orderId'):
            order_ids.append(trade.order.orderId)
        
        print(f"   Order {i+1}: {latency_ms:.3f}ms")
        time.sleep(0.1)
    
    # Cancel orders
    print("\n🧹 Cancelling orders...")
    for order_id in order_ids:
        try:
            ib.cancelOrder(order_id)
            print(f"   Cancelled {order_id}")
        except:
            pass
    
    avg_latency = sum(latencies) / len(latencies)
    print(f"\n📊 Results:")
    print(f"   Average latency: {avg_latency:.3f}ms")
    
    if avg_latency < 8:
        print(f"   ✅ Sub-8ms achieved!")
    
    ib.disconnect()
    return avg_latency


if __name__ == "__main__":
    print("🚀 NANO-TRADER TESTS")
    print("=" * 60)
    
    # Test 1: Connection pool
    test_pool_connections()
    
    # Test 2: Direct order latency (no pool)
    input("\nPress Enter to test direct order latency...")
    test_order_without_pool()