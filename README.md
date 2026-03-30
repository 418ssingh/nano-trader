\# 🚀 Nano-Trader: Sub-8ms Trading SDK for Interactive Brokers



\[!\[Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)

\[!\[Latency](https://img.shields.io/badge/Latency-0.633ms-brightgreen.svg)](https://github.com/418ssingh/nano-trader)

\[!\[License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



A \*\*high-performance trading SDK\*\* for Interactive Brokers API that achieves \*\*sub-8ms order latency\*\* - 12x faster than industry requirements.



\## 📊 Performance Metrics

╔═══════════════════════════════════════════════════════════════╗

║ NANO-TRADER PERFORMANCE ║

╠═══════════════════════════════════════════════════════════════╣

║ Average Order Latency: 0.633ms (Target: <8ms) ║

║ Min Order Latency: 0.354ms ║

║ Max Order Latency: 1.061ms (Still under 8ms!) ║

║ Sub-8ms Success Rate: 100% ║

║ Connection Pool Size: 3 persistent connections ║

║ Load Balancing: Round-robin ║

╚═══════════════════════════════════════════════════════════════╝



\## ✨ Features



\- \*\*⚡ Sub-8ms Order Execution\*\* - Average 0.633ms latency

\- \*\*🔌 Connection Pooling\*\* - Multiple persistent connections with round-robin load balancing

\- \*\*📊 Latency Tracking\*\* - P95, P99 metrics for performance monitoring

\- \*\*🔄 Auto-Reconnection\*\* - Handles connection failures gracefully

\- \*\*🎯 Production-Ready\*\* - Clean SDK design for quantitative traders



\## 📋 Requirements



\- Python 3.11+

\- Interactive Brokers Gateway or TWS

\- Interactive Brokers paper trading or live account



\## 🔧 Installation



```bash

\# Clone the repository

git clone https://github.com/418ssingh/nano-trader.git

cd nano-trader



🚀 Quick Start



\# Install dependencies

pip install ib\_async



from nano\_trader import ConnectionPool



\# Create connection pool

pool = ConnectionPool(host="127.0.0.1", port=4002, pool\_size=3)

pool.connect()



\# Place an order (0.633ms average latency)

trade, latency\_ms = pool.place\_limit\_order("AAPL", 100, 175.50, "BUY")

print(f"Order placed in {latency\_ms:.3f}ms")



\# Cancel order

pool.cancel\_order(trade.order.orderId)



\# Disconnect

pool.disconnect()



📈 Performance Test Results

Run the test script to verify performance:



bash

python test\_pool\_simple.py

Expected Output:



text

📝 Placing 5 test orders...

&#x20;  Order 1: 0.590ms

&#x20;  Order 2: 0.354ms

&#x20;  Order 3: 0.803ms

&#x20;  Order 4: 1.061ms

&#x20;  Order 5: 0.355ms



📊 Results:

&#x20;  Average latency: 0.633ms

&#x20;  ✅ Sub-8ms achieved!

🏗️ Architecture

text

┌─────────────────────────────────────────────────────────────┐

│                    Nano-Trader SDK                          │

├─────────────────────────────────────────────────────────────┤

│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │

│  │ Connection  │  │   Latency   │  │    Round-Robin      │ │

│  │    Pool     │  │   Tracker   │  │   Load Balancer     │ │

│  └─────────────┘  └─────────────┘  └─────────────────────┘ │

│         │               │                    │              │

│         ▼               ▼                    ▼              │

│  ┌─────────────────────────────────────────────────────┐   │

│  │           Interactive Brokers Gateway               │   │

│  │              (Paper Trading: Port 4002)             │   │

│  └─────────────────────────────────────────────────────┘   │

└─────────────────────────────────────────────────────────────┘

📁 Project Structure

text

nano-trader/

├── nano\_trader/

│   ├── core/

│   │   ├── connection\_pool.py    # Connection pool with latency tracking

│   │   └── latency\_tracker.py    # P95, P99 metrics

│   └── \_\_init\_\_.py               # SDK exports

├── test\_pool\_simple.py           # Performance demo

├── ZANSKAR\_QUALIFICATION\_REPORT.txt

└── README.md

🔧 Configuration

IB Gateway Setup

Open IB Gateway



Login with paper trading credentials



Go to Edit → Global Configuration → API → Settings



Enable Enable ActiveX and Socket Clients



Set port to 4002 (paper trading)



Add 127.0.0.1 to Trusted IPs



Restart IB Gateway



Connection Parameters

python

pool = ConnectionPool(

&#x20;   host="127.0.0.1",    # Local IB Gateway

&#x20;   port=4002,           # Paper trading port

&#x20;   pool\_size=3          # Number of persistent connections

)

📊 API Reference

ConnectionPool

Method	Description	Returns

connect()	Initialize connection pool	None

place\_limit\_order(symbol, qty, price, action)	Place limit order	(trade, latency\_ms)

cancel\_order(order\_id)	Cancel order	latency\_ms

get\_connection()	Get connection (context manager)	IB connection

disconnect()	Close all connections	None

print\_report()	Show performance report	None

LatencyTracker

Property	Description

stats.avg\_ms	Average latency

stats.p95\_ms	95th percentile latency

stats.p99\_ms	99th percentile latency

stats.sub\_8ms\_percent	Percentage under 8ms

🎯 Why Nano-Trader?

Requirement	Industry Standard	Nano-Trader

Order Latency	<8ms	0.633ms ✅

Connection Management	Single	Pooled (3+) ✅

Latency Monitoring	Basic	P95, P99 metrics ✅

Auto-Reconnection	❌	✅

📝 License

MIT License - Free for commercial and personal use



👨‍💻 Author

Shubham Singh - Algo Developer \& Quantitative Developer



GitHub: @418ssingh



Email: 418ssingh@gmail.com



🙏 Acknowledgments

Interactive Brokers for their API



Built for Zanskar Securities - Sub-8ms infrastructure requirement







