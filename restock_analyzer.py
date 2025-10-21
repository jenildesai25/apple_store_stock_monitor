#!/usr/bin/env python3
"""
Restock Pattern Analyzer - Track historical restock patterns to predict future availability
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import statistics


class RestockAnalyzer:
    """Analyze historical restock patterns to predict future availability."""

    def __init__(self, db_path: str = "restock_history.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the SQLite database for tracking restock history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS stock_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                store_code TEXT NOT NULL,
                product_code TEXT NOT NULL,
                available BOOLEAN NOT NULL,
                day_of_week INTEGER,
                hour_of_day INTEGER
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS restock_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                store_code TEXT NOT NULL,
                product_code TEXT NOT NULL,
                days_out_of_stock INTEGER,
                day_of_week INTEGER,
                hour_of_day INTEGER
            )
        """
        )

        conn.commit()
        conn.close()

    def record_stock_check(self, store_code: str, product_code: str, available: bool):
        """Record a stock availability check."""
        now = datetime.now()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if this is a restock event (was unavailable, now available)
        cursor.execute(
            """
            SELECT available FROM stock_checks 
            WHERE store_code = ? AND product_code = ? 
            ORDER BY timestamp DESC LIMIT 1
        """,
            (store_code, product_code),
        )

        last_check = cursor.fetchone()

        if last_check and not last_check[0] and available:
            # This is a restock event!
            cursor.execute(
                """
                SELECT COUNT(*) FROM stock_checks 
                WHERE store_code = ? AND product_code = ? 
                AND available = 0 AND timestamp > (
                    SELECT MAX(timestamp) FROM stock_checks 
                    WHERE store_code = ? AND product_code = ? AND available = 1
                )
            """,
                (store_code, product_code, store_code, product_code),
            )

            days_out = cursor.fetchone()[0] or 0

            cursor.execute(
                """
                INSERT INTO restock_events 
                (timestamp, store_code, product_code, days_out_of_stock, day_of_week, hour_of_day)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    now.isoformat(),
                    store_code,
                    product_code,
                    days_out,
                    now.weekday(),
                    now.hour,
                ),
            )

        # Record the stock check
        cursor.execute(
            """
            INSERT INTO stock_checks 
            (timestamp, store_code, product_code, available, day_of_week, hour_of_day)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                now.isoformat(),
                store_code,
                product_code,
                available,
                now.weekday(),
                now.hour,
            ),
        )

        conn.commit()
        conn.close()

    def get_restock_patterns(self, store_code: str, product_code: str) -> Dict:
        """Analyze restock patterns for a specific store/product combination."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get restock events
        cursor.execute(
            """
            SELECT day_of_week, hour_of_day, days_out_of_stock, timestamp
            FROM restock_events 
            WHERE store_code = ? AND product_code = ?
            ORDER BY timestamp DESC
        """,
            (store_code, product_code),
        )

        events = cursor.fetchall()
        conn.close()

        if not events:
            return {"message": "No restock history available"}

        # Analyze patterns
        days_of_week = [event[0] for event in events]
        hours = [event[1] for event in events]
        out_of_stock_periods = [event[2] for event in events]

        day_names = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        return {
            "total_restocks": len(events),
            "most_common_day": (
                day_names[statistics.mode(days_of_week)] if days_of_week else None
            ),
            "average_restock_hour": statistics.mean(hours) if hours else None,
            "average_days_out_of_stock": (
                statistics.mean(out_of_stock_periods) if out_of_stock_periods else None
            ),
            "last_restock": events[0][3] if events else None,
            "restock_frequency_days": self._calculate_restock_frequency(events),
        }

    def _calculate_restock_frequency(self, events: List) -> Optional[float]:
        """Calculate average days between restocks."""
        if len(events) < 2:
            return None

        timestamps = [datetime.fromisoformat(event[3]) for event in events]
        timestamps.sort()

        intervals = []
        for i in range(1, len(timestamps)):
            interval = (timestamps[i] - timestamps[i - 1]).days
            intervals.append(interval)

        return statistics.mean(intervals) if intervals else None

    def predict_next_restock(self, store_code: str, product_code: str) -> Dict:
        """Predict when the next restock might occur."""
        patterns = self.get_restock_patterns(store_code, product_code)

        if "message" in patterns:
            return {"prediction": "Insufficient data for prediction"}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get current stock status
        cursor.execute(
            """
            SELECT available, timestamp FROM stock_checks 
            WHERE store_code = ? AND product_code = ? 
            ORDER BY timestamp DESC LIMIT 1
        """,
            (store_code, product_code),
        )

        current_status = cursor.fetchone()
        conn.close()

        if not current_status:
            return {"prediction": "No stock data available"}

        is_available, last_check = current_status

        if is_available:
            return {"prediction": "Currently in stock"}

        # Calculate prediction based on patterns
        prediction = {}

        if patterns.get("restock_frequency_days"):
            last_restock = datetime.fromisoformat(patterns["last_restock"])
            avg_frequency = patterns["restock_frequency_days"]
            next_estimated = last_restock + timedelta(days=avg_frequency)
            prediction["estimated_date"] = next_estimated.strftime("%Y-%m-%d")

        if patterns.get("most_common_day"):
            prediction["likely_day"] = patterns["most_common_day"]

        if patterns.get("average_restock_hour"):
            hour = int(patterns["average_restock_hour"])
            prediction["likely_time"] = f"{hour:02d}:00"

        return prediction


def main():
    """Example usage of the restock analyzer."""
    analyzer = RestockAnalyzer()

    # Example: Analyze Washington Square iPhone 15 Pro patterns
    store_code = "R090"  # Washington Square
    product_code = "MU2F3LL/A"  # iPhone 15 Pro 128GB Natural Titanium

    patterns = analyzer.get_restock_patterns(store_code, product_code)
    print("Restock Patterns:")
    print(json.dumps(patterns, indent=2))

    prediction = analyzer.predict_next_restock(store_code, product_code)
    print("\nNext Restock Prediction:")
    print(json.dumps(prediction, indent=2))


if __name__ == "__main__":
    main()
