"""
World Bank API Data Ingestion for Senegal
Fetches development indicators from World Bank Open Data API
NO API KEY REQUIRED - Completely free and open!
"""
import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict
from pathlib import Path
import time

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import setup_logger

logger = setup_logger('worldbank_ingestion')


class WorldBankDataCollector:
    """Collect development data for Senegal from World Bank API"""
    
    BASE_URL = "https://api.worldbank.org/v2"
    COUNTRY_CODE = "SN"  # Senegal ISO code
    
    # Comprehensive list of indicators for Senegal
    INDICATORS = {
        # Economic Indicators
        'NY.GDP.MKTP.KD.ZG': 'GDP Growth (annual %)',
        'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
        'NY.GDP.MKTP.CD': 'GDP (current US$)',
        'FP.CPI.TOTL.ZG': 'Inflation (CPI annual %)',
        'NE.EXP.GNFS.ZS': 'Exports of goods and services (% of GDP)',
        'NE.IMP.GNFS.ZS': 'Imports of goods and services (% of GDP)',
        'BX.KLT.DINV.WD.GD.ZS': 'Foreign direct investment (% of GDP)',
        
        # Population & Demographics
        'SP.POP.TOTL': 'Population, total',
        'SP.POP.GROW': 'Population growth (annual %)',
        'SP.URB.TOTL.IN.ZS': 'Urban population (% of total)',
        'SP.DYN.LE00.IN': 'Life expectancy at birth (years)',
        'SP.DYN.TFRT.IN': 'Fertility rate (births per woman)',
        
        # Poverty & Inequality
        'SI.POV.DDAY': 'Poverty headcount ratio at $2.15 a day',
        'SI.POV.NAHC': 'Poverty headcount ratio (national poverty lines)',
        'NY.GNP.PCAP.CD': 'GNI per capita (current US$)',
        
        # Education
        'SE.ADT.LITR.ZS': 'Literacy rate, adult total (% of people ages 15+)',
        'SE.PRM.NENR': 'School enrollment, primary (% net)',
        'SE.SEC.NENR': 'School enrollment, secondary (% net)',
        'SE.XPD.TOTL.GD.ZS': 'Government expenditure on education (% of GDP)',
        
        # Health
        'SH.DYN.MORT': 'Mortality rate, under-5 (per 1,000 live births)',
        'SH.STA.MMRT': 'Maternal mortality ratio (per 100,000 live births)',
        'SH.XPD.CHEX.GD.ZS': 'Current health expenditure (% of GDP)',
        'SH.H2O.BASW.ZS': 'People using at least basic drinking water services',
        
        # Infrastructure & Technology
        'EG.ELC.ACCS.ZS': 'Access to electricity (% of population)',
        'IT.NET.USER.ZS': 'Individuals using the Internet (% of population)',
        'IT.CEL.SETS.P2': 'Mobile cellular subscriptions (per 100 people)',
        'IS.ROD.PAVE.ZS': 'Roads, paved (% of total roads)',
        
        # Agriculture & Environment
        'AG.LND.AGRI.ZS': 'Agricultural land (% of land area)',
        'AG.PRD.CROP.XD': 'Crop production index',
        'NV.AGR.TOTL.ZS': 'Agriculture value added (% of GDP)',
        'EN.ATM.CO2E.PC': 'CO2 emissions (metric tons per capita)',
    }
    
    def __init__(self):
        logger.info(f"Initialized World Bank collector for Senegal")
        logger.info(f"Will collect {len(self.INDICATORS)} indicators")
    
    def get_indicator_data(self, indicator_code: str, start_year: int = 1960, end_year: int = None) -> pd.DataFrame:
        """
        Fetch time series data for a given World Bank indicator
        
        Args:
            indicator_code: World Bank indicator code
            start_year: Start year for data
            end_year: End year for data (defaults to current year)
        
        Returns:
            DataFrame with year and value columns
        """
        if end_year is None:
            end_year = datetime.now().year
        
        # World Bank API URL structure
        url = f"{self.BASE_URL}/country/{self.COUNTRY_CODE}/indicator/{indicator_code}"
        
        params = {
            'format': 'json',
            'date': f'{start_year}:{end_year}',
            'per_page': 1000  # Get all data
        }
        
        try:
            logger.info(f"Fetching data for indicator: {indicator_code}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # World Bank returns [metadata, data]
            if len(data) < 2 or not data[1]:
                logger.warning(f"No data found for indicator {indicator_code}")
                return pd.DataFrame()
            
            records = data[1]
            
            # Convert to DataFrame
            df_data = []
            for record in records:
                if record['value'] is not None:  # Skip null values
                    df_data.append({
                        'year': int(record['date']),
                        'value': float(record['value']),
                        'indicator_code': indicator_code,
                        'indicator_name': self.INDICATORS.get(indicator_code, indicator_code),
                        'country': record['country']['value'],
                        'country_code': record['countryiso3code']
                    })
            
            if not df_data:
                logger.warning(f"No valid data points for {indicator_code}")
                return pd.DataFrame()
            
            df = pd.DataFrame(df_data)
            logger.info(f"Successfully fetched {len(df)} observations for {indicator_code}")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {indicator_code}: {e}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Unexpected error for {indicator_code}: {e}")
            return pd.DataFrame()
    
    def get_country_metadata(self) -> Dict:
        """Get metadata about Senegal"""
        url = f"{self.BASE_URL}/country/{self.COUNTRY_CODE}"
        params = {'format': 'json'}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if len(data) > 1 and data[1]:
                country_info = data[1][0]
                return {
                    'name': country_info.get('name'),
                    'capital': country_info.get('capitalCity'),
                    'region': country_info.get('region', {}).get('value'),
                    'income_level': country_info.get('incomeLevel', {}).get('value'),
                    'longitude': country_info.get('longitude'),
                    'latitude': country_info.get('latitude')
                }
        except Exception as e:
            logger.error(f"Error fetching country metadata: {e}")
        
        return {}
    
    def collect_all_indicators(self, start_year: int = 1960, end_year: int = None) -> pd.DataFrame:
        """
        Collect all configured development indicators for Senegal
        
        Args:
            start_year: Start year for data collection (Senegal independence: 1960)
            end_year: End year for data collection (defaults to current year)
        
        Returns:
            Combined DataFrame with all indicators
        """
        if end_year is None:
            end_year = datetime.now().year
        
        logger.info(f"Collecting data from {start_year} to {end_year}")
        
        all_data = []
        successful = 0
        failed = 0
        
        for indicator_code in self.INDICATORS.keys():
            df = self.get_indicator_data(indicator_code, start_year, end_year)
            
            if not df.empty:
                all_data.append(df)
                successful += 1
            else:
                failed += 1
            
            # Rate limiting - be nice to the API
            time.sleep(0.3)
        
        logger.info(f"Collection complete: {successful} successful, {failed} failed")
        
        if not all_data:
            logger.error("No data collected from any indicator")
            return pd.DataFrame()
        
        # Combine all indicators
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df['ingestion_timestamp'] = datetime.now()
        
        # Add country metadata
        metadata = self.get_country_metadata()
        for key, value in metadata.items():
            combined_df[f'country_{key}'] = value
        
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
    logger.info("Starting World Bank data collection for Senegal")
    
    collector = WorldBankDataCollector()
    
    # Collect data from independence (1960) to present
    df = collector.collect_all_indicators(start_year=1960)
    
    if df.empty:
        logger.error("No data collected, exiting")
        return
    
    # Save to local file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    output_file = output_dir / f"senegal_worldbank_data_{timestamp}.parquet"
    
    collector.save_to_file(df, output_file)
    
    # Print summary
    print("\n" + "="*70)
    print("World Bank Data Collection Summary - SENEGAL")
    print("="*70)
    print(f"Country: Senegal (SN)")
    print(f"Total records: {len(df):,}")
    print(f"Year range: {df['year'].min()} to {df['year'].max()}")
    print(f"Indicators collected: {df['indicator_code'].nunique()}")
    print(f"\nTop 10 indicators by data points:")
    print(df['indicator_name'].value_counts().head(10))
    print("\n" + "="*70)
    print("✅ NO API KEY REQUIRED - World Bank API is completely free!")
    print("="*70)
    
    logger.info("World Bank data collection completed successfully")


if __name__ == "__main__":
    main()

