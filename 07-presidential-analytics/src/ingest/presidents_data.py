"""
Presidential Data Collection
Compiles US presidential terms and administration information
"""
import pandas as pd
from datetime import datetime
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import setup_logger

logger = setup_logger('presidents_ingestion')


class PresidentsDataCollector:
    """Collect and structure US Presidential data"""
    
    def __init__(self):
        self.presidents_data = self._get_presidents_data()
        logger.info(f"Initialized with {len(self.presidents_data)} presidents")
    
    def _get_presidents_data(self) -> list:
        """
        Comprehensive presidential data since 1945 (end of WW2)
        Data includes: name, party, start date, end date, key achievements
        """
        return [
            {
                'president_id': 33,
                'name': 'Harry S. Truman',
                'party': 'Democratic',
                'start_date': '1945-04-12',
                'end_date': '1953-01-20',
                'terms': 2,
                'key_policies': 'Marshall Plan, NATO, Fair Deal, Korean War'
            },
            {
                'president_id': 34,
                'name': 'Dwight D. Eisenhower',
                'party': 'Republican',
                'start_date': '1953-01-20',
                'end_date': '1961-01-20',
                'terms': 2,
                'key_policies': 'Interstate Highway System, Civil Rights Act of 1957'
            },
            {
                'president_id': 35,
                'name': 'John F. Kennedy',
                'party': 'Democratic',
                'start_date': '1961-01-20',
                'end_date': '1963-11-22',
                'terms': 1,
                'key_policies': 'Space Program, Peace Corps, Civil Rights'
            },
            {
                'president_id': 36,
                'name': 'Lyndon B. Johnson',
                'party': 'Democratic',
                'start_date': '1963-11-22',
                'end_date': '1969-01-20',
                'terms': 1,
                'key_policies': 'Great Society, Medicare, Civil Rights Act of 1964'
            },
            {
                'president_id': 37,
                'name': 'Richard Nixon',
                'party': 'Republican',
                'start_date': '1969-01-20',
                'end_date': '1974-08-09',
                'terms': 2,
                'key_policies': 'EPA, China Relations, Watergate'
            },
            {
                'president_id': 38,
                'name': 'Gerald Ford',
                'party': 'Republican',
                'start_date': '1974-08-09',
                'end_date': '1977-01-20',
                'terms': 1,
                'key_policies': 'Nixon Pardon, Helsinki Accords'
            },
            {
                'president_id': 39,
                'name': 'Jimmy Carter',
                'party': 'Democratic',
                'start_date': '1977-01-20',
                'end_date': '1981-01-20',
                'terms': 1,
                'key_policies': 'Camp David Accords, Energy Policy, Iran Hostage Crisis'
            },
            {
                'president_id': 40,
                'name': 'Ronald Reagan',
                'party': 'Republican',
                'start_date': '1981-01-20',
                'end_date': '1989-01-20',
                'terms': 2,
                'key_policies': 'Reaganomics, Cold War Escalation, Tax Cuts'
            },
            {
                'president_id': 41,
                'name': 'George H. W. Bush',
                'party': 'Republican',
                'start_date': '1989-01-20',
                'end_date': '1993-01-20',
                'terms': 1,
                'key_policies': 'Gulf War, Fall of USSR, ADA Act'
            },
            {
                'president_id': 42,
                'name': 'Bill Clinton',
                'party': 'Democratic',
                'start_date': '1993-01-20',
                'end_date': '2001-01-20',
                'terms': 2,
                'key_policies': 'NAFTA, Budget Surplus, Tech Boom'
            },
            {
                'president_id': 43,
                'name': 'George W. Bush',
                'party': 'Republican',
                'start_date': '2001-01-20',
                'end_date': '2009-01-20',
                'terms': 2,
                'key_policies': '9/11 Response, Iraq War, Medicare Part D, Financial Crisis'
            },
            {
                'president_id': 44,
                'name': 'Barack Obama',
                'party': 'Democratic',
                'start_date': '2009-01-20',
                'end_date': '2017-01-20',
                'terms': 2,
                'key_policies': 'ACA (Obamacare), Economic Recovery, Paris Climate Agreement'
            },
            {
                'president_id': 45,
                'name': 'Donald Trump',
                'party': 'Republican',
                'start_date': '2017-01-20',
                'end_date': '2021-01-20',
                'terms': 1,
                'key_policies': 'Tax Cuts, Tariffs, COVID-19 Response'
            },
            {
                'president_id': 46,
                'name': 'Joe Biden',
                'party': 'Democratic',
                'start_date': '2021-01-20',
                'end_date': None,  # Current president
                'terms': 1,
                'key_policies': 'Infrastructure Bill, COVID Relief, Climate Action'
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
    print("\n" + "="*60)
    print("Presidential Data Collection Summary")
    print("="*60)
    print(f"Total presidents: {len(presidents_df)}")
    print(f"Date range: {presidents_df['start_date'].min()} to {datetime.now().strftime('%Y-%m-%d')}")
    print(f"\nPresidents by party:")
    print(presidents_df['party'].value_counts())
    print(f"\nAverage tenure: {presidents_df['tenure_days'].mean():.0f} days")
    print("="*60)
    
    logger.info("Presidential data collection completed successfully")


if __name__ == "__main__":
    main()

