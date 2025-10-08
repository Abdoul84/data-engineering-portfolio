#!/usr/bin/env python3
"""
Test FRED API connection and data collection
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from ingest.fred_api import FREDDataCollector

def test_fred_api():
    """Test FRED API connection and data collection"""
    try:
        print("🔗 Testing FRED API connection...")
        
        # Initialize FRED collector
        collector = FREDDataCollector()
        print(f"✅ FRED API key configured: {collector.api_key[:8]}...")
        
        # Test getting GDP data
        print("\n📊 Testing GDP data collection...")
        gdp_data = collector.get_series_data("GDP", "2020-01-01", "2024-01-01")
        print(f"✅ Retrieved {len(gdp_data)} GDP data points")
        print(f"Latest GDP: ${gdp_data['value'].iloc[-1]:,.0f}B")
        
        # Test getting unemployment rate
        print("\n📈 Testing unemployment rate data...")
        unrate_data = collector.get_series_data("UNRATE", "2020-01-01", "2024-01-01")
        print(f"✅ Retrieved {len(unrate_data)} unemployment data points")
        print(f"Latest unemployment rate: {unrate_data['value'].iloc[-1]:.1f}%")
        
        # Test collecting all configured metrics
        print("\n🎯 Testing all configured metrics...")
        all_data = collector.collect_all_metrics()
        print(f"✅ Collected data for {len(all_data)} metrics")
        
        for metric_name, data in all_data.items():
            print(f"  - {metric_name}: {len(data)} data points")
        
        print("\n🎉 FRED API test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ FRED API test failed: {e}")
        return False

if __name__ == "__main__":
    test_fred_api()
