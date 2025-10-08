"""
FRED API Data Ingestion
Fetches economic indicators from Federal Reserve Economic Data
"""
import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict
from pathlib import Path
import time

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import get_config
from utils.logger import setup_logger

logger = setup_logger('fred_ingestion')


class FREDDataCollector:
    """Collect economic data from FRED API"""
    
    BASE_URL = "https://api.stlouisfed.org/fred"
    
    def __init__(self):
        self.config = get_config()
        self.api_key = self.config.fred_api_key
        
        if not self.api_key or self.api_key == "0fc3240db258c98d21d6c3efb2c699e7":
            raise ValueError(
                "FRED API key not configured. "
                "Get a free key from https://fred.stlouisfed.org/docs/api/api_key.html"
            )
        
        self.metrics = self.config.fred_metrics
        logger.info(f"Initialized FRED collector with {len(self.metrics)} metrics")
    
    def get_series_data(self, series_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Fetch time series data for a given FRED series
        
        Args:
            series_id: FRED series identifier (e.g., 'GDP', 'UNRATE')
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        
        Returns:
            DataFrame with date and value columns
        """
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json'
        }
        
        if start_date:
            params['observation_start'] = start_date
        if end_date:
            params['observation_end'] = end_date
        
        url = f"{self.BASE_URL}/series/observations"
        
        try:
            logger.info(f"Fetching data for series: {series_id}")
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            observations = data.get('observations', [])
            
            if not observations:
                logger.warning(f"No data found for series {series_id}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(observations)
            df = df[['date', 'value']]
            df['series_id'] = series_id
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            
            # Get series metadata
            df['series_name'] = self.get_series_info(series_id).get('title', series_id)
            
            logger.info(f"Successfully fetched {len(df)} observations for {series_id}")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {series_id}: {e}")
            return pd.DataFrame()
    
    def get_series_info(self, series_id: str) -> Dict:
        """Get metadata for a FRED series"""
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json'
        }
        
        url = f"{self.BASE_URL}/series"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('seriess', [{}])[0]
        except Exception as e:
            logger.error(f"Error fetching metadata for {series_id}: {e}")
            return {}
    
    def collect_all_metrics(self, start_date: str = "1945-01-01", end_date: str = None) -> pd.DataFrame:
        """
        Collect all configured economic metrics
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection (defaults to today)
        
        Returns:
            Combined DataFrame with all metrics
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        all_data = []
        
        for metric in self.metrics:
            series_id = metric['series_id'] if isinstance(metric, dict) else metric
            df = self.get_series_data(series_id, start_date, end_date)
            
            if not df.empty:
                all_data.append(df)
            
            # Rate limiting - be nice to the API
            time.sleep(0.5)
        
        if not all_data:
            logger.error("No data collected from any series")
            return pd.DataFrame()
        
        # Combine all series
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df['ingestion_timestamp'] = datetime.now()
        
        logger.info(f"Total records collected: {len(combined_df)}")
        return combined_df
    
    def save_to_file(self, df: pd.DataFrame, output_path: str):
        """Save data to parquet file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_parquet(output_path, index=False, compression='snappy')
        logger.info(f"Data saved to {output_path}")


def main():
    """Main execution function"""
    logger.info("Starting FRED data collection")
    
    collector = FREDDataCollector()
    
    # Collect data
    df = collector.collect_all_metrics()
    
    if df.empty:
        logger.error("No data collected, exiting")
        return
    
    # Save to local file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    output_file = output_dir / f"fred_economic_data_{timestamp}.parquet"
    
    collector.save_to_file(df, output_file)
    
    # Print summary
    print("\n" + "="*60)
    print("FRED Data Collection Summary")
    print("="*60)
    print(f"Total records: {len(df):,}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Series collected: {df['series_id'].nunique()}")
    print(f"\nSeries breakdown:")
    print(df.groupby('series_id').size())
    print("="*60)
    
    logger.info("FRED data collection completed successfully")


if __name__ == "__main__":
    main()

