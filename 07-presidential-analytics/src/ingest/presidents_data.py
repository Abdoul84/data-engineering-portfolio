"""
Presidential Data Collection - SENEGAL
Compiles Senegalese presidential terms and administration information
From independence (1960) to present
"""
import pandas as pd
from datetime import datetime
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import setup_logger

logger = setup_logger('presidents_ingestion')


class PresidentsDataCollector:
    """Collect and structure Senegalese Presidential data"""
    
    def __init__(self):
        self.presidents_data = self._get_presidents_data()
        logger.info(f"Initialized with {len(self.presidents_data)} Senegalese presidents")
    
    def _get_presidents_data(self) -> list:
        """
        Comprehensive presidential data since independence (1960)
        Senegal - A model African democracy with peaceful transitions
        Data includes: name, party, start date, end date, key achievements
        """
        return [
            {
                'president_id': 1,
                'name': 'Léopold Sédar Senghor',
                'party': 'Union Progressiste Sénégalaise (UPS)',
                'start_date': '1960-09-05',  # Independence Day
                'end_date': '1980-12-31',
                'terms': 4,
                'key_policies': 'Post-independence nation building, Negritude philosophy, Agricultural development, Francophonie leadership',
                'notable': 'Poet-president, voluntarily stepped down'
            },
            {
                'president_id': 2,
                'name': 'Abdou Diouf',
                'party': 'Parti Socialiste (PS)',
                'start_date': '1981-01-01',
                'end_date': '2000-04-01',
                'terms': 3,
                'key_policies': 'Economic liberalization, Multi-party democracy, Regional integration (ECOWAS), Structural adjustment programs',
                'notable': 'Peaceful transition after electoral defeat - rare in Africa'
            },
            {
                'president_id': 3,
                'name': 'Abdoulaye Wade',
                'party': 'Parti Démocratique Sénégalais (PDS)',
                'start_date': '2000-04-01',
                'end_date': '2012-04-02',
                'terms': 2,
                'key_policies': 'Infrastructure modernization (highways, airport), NEPAD initiative, Constitutional reforms, Dakar Port expansion',
                'notable': 'First opposition candidate to win presidency'
            },
            {
                'president_id': 4,
                'name': 'Macky Sall',
                'party': 'Alliance pour la République (APR)',
                'start_date': '2012-04-02',
                'end_date': '2024-04-02',
                'terms': 2,
                'key_policies': 'Plan Sénégal Émergent (PSE), Infrastructure investments, Oil & gas development, Education reforms, COVID-19 response',
                'notable': 'Committed to not running for 3rd term, respected term limits'
            },
            {
                'president_id': 5,
                'name': 'Bassirou Diomaye Faye',
                'party': 'PASTEF (Patriotes Africains du Sénégal)',
                'start_date': '2024-04-02',
                'end_date': None,  # Current president
                'terms': 1,
                'key_policies': 'Economic sovereignty, Anti-corruption, Youth employment, Natural resources renegotiation',
                'notable': 'Youngest elected president in Senegal, released from prison to run'
            }
        ]
    
    def get_dataframe(self) -> pd.DataFrame:
        """Convert presidents data to DataFrame"""
        df = pd.DataFrame(self.presidents_data)
        
        # Convert dates
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])
        
        # Calculate tenure in days
        df['tenure_days'] = (df['end_date'] - df['start_date']).dt.days
        
        # For current president, use today's date for tenure calculation
        current_mask = df['end_date'].isna()
        df.loc[current_mask, 'tenure_days'] = (datetime.now() - df.loc[current_mask, 'start_date']).dt.days
        
        # Add metadata
        df['ingestion_timestamp'] = datetime.now()
        df['is_current'] = df['end_date'].isna()
        
        logger.info(f"Created DataFrame with {len(df)} presidents")
        return df
    
    def get_president_date_mapping(self) -> pd.DataFrame:
        """
        Create a mapping of every date to the sitting president
        Useful for joining with economic time series data
        """
        df = self.get_dataframe()
        date_mappings = []
        
        for _, row in df.iterrows():
            start = row['start_date']
            end = row['end_date'] if pd.notna(row['end_date']) else datetime.now()
            
            # Generate all dates in this president's term
            date_range = pd.date_range(start=start, end=end, freq='D')
            
            for date in date_range:
                date_mappings.append({
                    'date': date,
                    'president_id': row['president_id'],
                    'president_name': row['name'],
                    'party': row['party']
                })
        
        mapping_df = pd.DataFrame(date_mappings)
        logger.info(f"Created date mapping with {len(mapping_df)} rows")
        return mapping_df
    
    def save_to_file(self, df: pd.DataFrame, output_path: str):
        """Save data to parquet file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_parquet(output_path, index=False, compression='snappy')
        logger.info(f"Data saved to {output_path}")


def main():
    """Main execution function"""
    logger.info("Starting presidential data collection")
    
    collector = PresidentsDataCollector()
    
    # Get presidents DataFrame
    presidents_df = collector.get_dataframe()
    
    # Get date mapping DataFrame
    date_mapping_df = collector.get_president_date_mapping()
    
    # Save both files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    
    presidents_file = output_dir / f"presidents_{timestamp}.parquet"
    mapping_file = output_dir / f"president_date_mapping_{timestamp}.parquet"
    
    collector.save_to_file(presidents_df, presidents_file)
    collector.save_to_file(date_mapping_df, mapping_file)
    
    # Print summary
    print("\n" + "="*70)
    print("Presidential Data Collection Summary - SENEGAL")
    print("="*70)
    print(f"Country: Senegal (Independence: September 5, 1960)")
    print(f"Total presidents: {len(presidents_df)}")
    print(f"Date range: {presidents_df['start_date'].min()} to {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Years of democracy: {(datetime.now() - presidents_df['start_date'].min()).days / 365:.1f} years")
    print(f"\nPresidents by party:")
    print(presidents_df['party'].value_counts())
    print(f"\nAverage tenure: {presidents_df['tenure_days'].mean():.0f} days ({presidents_df['tenure_days'].mean()/365:.1f} years)")
    print("\n🇸🇳 Senegal: A model of African democracy with peaceful transitions")
    print("="*70)
    
    logger.info("Presidential data collection completed successfully")


if __name__ == "__main__":
    main()

