#!/usr/bin/env python3
"""
Test Snowflake connection and data loading
"""
import snowflake.connector
import yaml
import pandas as pd
from pathlib import Path

def test_snowflake_connection():
    """Test Snowflake connection and basic queries"""
    
    # Load config
    config_path = Path(__file__).parent / "config" / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)['snowflake']
    
    print("🔗 Testing Snowflake connection...")
    print(f"Account: {config['account']}")
    print(f"User: {config['user']}")
    print(f"Database: {config['database']}")
    print(f"Schema: {config['schema']}")
    
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            account=config['account'],
            user=config['user'],
            password=config['password'],
            warehouse=config['warehouse'],
            database=config['database'],
            schema=config['schema']
        )
        
        print("✅ Connected to Snowflake successfully!")
        
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()")
        result = cursor.fetchone()
        print(f"📍 Current: {result[0]}.{result[1]} @ {result[2]}")
        
        # Test presidents table
        cursor.execute("SELECT COUNT(*) FROM presidents_dim")
        pres_count = cursor.fetchone()[0]
        print(f"👥 Presidents table: {pres_count} records")
        
        # Test development_facts table
        cursor.execute("SELECT COUNT(*) FROM development_facts")
        dev_count = cursor.fetchone()[0]
        print(f"📊 Development facts table: {dev_count} records")
        
        # Test sample data
        cursor.execute("SELECT PRESIDENT_NAME, PARTY FROM presidents_dim LIMIT 3")
        presidents = cursor.fetchall()
        print("📋 Sample presidents:")
        for pres in presidents:
            print(f"  - {pres[0]} ({pres[1]})")
        
        cursor.close()
        conn.close()
        
        print("🎉 All tests passed! Snowflake connection is working.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_snowflake_connection()
