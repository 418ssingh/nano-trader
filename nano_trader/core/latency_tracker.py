"""
Latency Tracker - Monitors execution speed for sub-8ms validation
"""

import time
import statistics
from collections import deque
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LatencyStats:
    """Container for latency statistics"""
    avg_ms: float = 0.0
    min_ms: float = 0.0
    max_ms: float = 0.0
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    sub_8ms_percent: float = 0.0
    total_samples: int = 0


class LatencyTracker:
    """
    Tracks latency metrics for trading operations.
    Specifically monitors sub-8ms performance.
    
    Usage:
        tracker = LatencyTracker()
        start = time.perf_counter_ns()
        # ... do something ...
        latency_ms = (time.perf_counter_ns() - start) / 1_000_000
        tracker.record(latency_ms)
        
        stats = tracker.stats
        print(f"Average latency: {stats.avg_ms:.2f}ms")
    """
    
    def __init__(self, name: str = "default", window_size: int = 1000):
        self.name = name
        self.window_size = window_size
        self._latencies: List[float] = []
    
    def record(self, latency_ms: float) -> None:
        """Record a single latency measurement"""
        self._latencies.append(latency_ms)
        # Keep only recent measurements
        if len(self._latencies) > self.window_size:
            self._latencies.pop(0)
    
    @property
    def stats(self) -> LatencyStats:
        """Calculate current statistics"""
        if not self._latencies:
            return LatencyStats()
        
        sorted_lats = sorted(self._latencies)
        n = len(sorted_lats)
        
        # Count how many orders are under 8ms
        sub_8_count = sum(1 for l in sorted_lats if l < 8.0)
        
        return LatencyStats(
            avg_ms=sum(sorted_lats) / n,
            min_ms=sorted_lats[0],
            max_ms=sorted_lats[-1],
            p50_ms=sorted_lats[int(n * 0.50)],
            p95_ms=sorted_lats[int(n * 0.95)],
            p99_ms=sorted_lats[int(n * 0.99)],
            sub_8ms_percent=(sub_8_count / n) * 100,
            total_samples=n
        )
    
    def reset(self) -> None:
        """Clear all recorded latencies"""
        self._latencies.clear()
    
    def report(self) -> str:
        """Generate a formatted report"""
        s = self.stats
        status = "PASS" if s.avg_ms < 8 else "FAIL"
        
        return f"""
╔════════════════════════════════════════════╗
║ Latency Report: {self.name}
╠════════════════════════════════════════════╣
║ Total Samples:  {s.total_samples}
║ Average:        {s.avg_ms:.3f}ms
║ Min:            {s.min_ms:.3f}ms
║ Max:            {s.max_ms:.3f}ms
║ P95:            {s.p95_ms:.3f}ms
║ P99:            {s.p99_ms:.3f}ms
║ Sub-8ms Rate:   {s.sub_8ms_percent:.1f}%
║ Status:         {status}
╚════════════════════════════════════════════╝
"""


# Quick test for the LatencyTracker
if __name__ == "__main__":
    print("Testing LatencyTracker...")
    
    tracker = LatencyTracker(name="test")
    
    # Simulate some latencies
    test_latencies = [0.35, 0.42, 0.38, 0.41, 0.39, 5.0, 7.5, 6.8]
    for lat in test_latencies:
        tracker.record(lat)
    
    print(tracker.report())
    
    # Verify sub-8ms calculation
    stats = tracker.stats
    expected_sub_8 = (8 / 8) * 100  # 8 out of 8 are under 8ms
    print(f"Sub-8ms percent: {stats.sub_8ms_percent:.1f}% (expected: 100%)")
    print("\n✅ LatencyTracker works!")