#!/usr/bin/env python3
"""
Debug what data we actually have in Snowflake
"""
import snowflake.connector
import yaml
import pandas as pd
from pathlib import Path

def debug_snowflake_data():
    """Debug what data we actually have in Snowflake"""
    
    # Load config
    config_path = Path(__file__).parent / "config" / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)['snowflake']
    
    print("🔍 Debugging Snowflake data...")
    
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
        
        cursor = conn.cursor()
        
        # Check what tables we have
        print("\n📋 Available tables:")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            print(f"  - {table[1]}")
        
        # Check presidents data
        print(f"\n👥 Presidents data:")
        cursor.execute("SELECT COUNT(*) FROM presidents_dim")
        pres_count = cursor.fetchone()[0]
        print(f"  Total presidents: {pres_count}")
        
        cursor.execute("SELECT PRESIDENT_NAME, PARTY FROM presidents_dim LIMIT 3")
        presidents = cursor.fetchall()
        for pres in presidents:
            print(f"  - {pres[0]} ({pres[1]})")
        
        # Check development_facts data
        print(f"\n📊 Development facts data:")
        cursor.execute("SELECT COUNT(*) FROM development_facts")
        dev_count = cursor.fetchone()[0]
        print(f"  Total development records: {dev_count}")
        
        # Check what indicators we have
        cursor.execute("SELECT DISTINCT INDICATOR_CODE, INDICATOR_NAME FROM development_facts LIMIT 10")
        indicators = cursor.fetchall()
        print(f"  Sample indicators:")
        for ind in indicators:
            print(f"    - {ind[0]}: {ind[1]}")
        
        # Check what countries we have
        cursor.execute("SELECT DISTINCT COUNTRY_CODE, COUNTRY FROM development_facts")
        countries = cursor.fetchall()
        print(f"  Countries in data:")
        for country in countries:
            print(f"    - {country[0]}: {country[1]}")
        
        # Check years range
        cursor.execute("SELECT MIN(YEAR), MAX(YEAR) FROM development_facts")
        year_range = cursor.fetchone()
        print(f"  Year range: {year_range[0]} - {year_range[1]}")
        
        # Check Senegal specifically
        cursor.execute("SELECT COUNT(*) FROM development_facts WHERE COUNTRY_CODE = 'SN'")
        sen_count = cursor.fetchone()[0]
        print(f"  Senegal records: {sen_count}")
        
        if sen_count > 0:
            cursor.execute("SELECT DISTINCT INDICATOR_CODE, INDICATOR_NAME FROM development_facts WHERE COUNTRY_CODE = 'SN' LIMIT 10")
            sen_indicators = cursor.fetchall()
            print(f"  Senegal indicators:")
            for ind in sen_indicators:
                print(f"    - {ind[0]}: {ind[1]}")
        
        # Check if we have population tables
        print(f"\n🏠 Population tables:")
        try:
            cursor.execute("SELECT COUNT(*) FROM ansd_population")
            ansd_count = cursor.fetchone()[0]
            print(f"  ANSD population records: {ansd_count}")
        except:
            print("  No ANSD population table found")
        
        try:
            cursor.execute("SELECT COUNT(*) FROM ansd_demographics")
            demo_count = cursor.fetchone()[0]
            print(f"  ANSD demographics records: {demo_count}")
        except:
            print("  No ANSD demographics table found")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_snowflake_data()
