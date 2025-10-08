"""
Snowflake Data Loader for Senegal Presidential Analytics
Loads data from local parquet files into Snowflake tables
"""
import snowflake.connector
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.config import get_config
from utils.logger import setup_logger

logger = setup_logger('snowflake_loader')


class SnowflakeLoader:
    """Load data into Snowflake data warehouse"""
    
    def __init__(self):
        self.config = get_config()
        sf_config = self.config.snowflake_config
        
        logger.info("Connecting to Snowflake...")
        try:
            self.conn = snowflake.connector.connect(
                account=sf_config.get('account'),
                user=sf_config.get('user'),
                password=sf_config.get('password'),
                warehouse=sf_config.get('warehouse', 'COMPUTE_WH'),
                database=sf_config.get('database', 'SENEGAL_ANALYTICS'),
                schema=sf_config.get('schema', 'PUBLIC'),
                role=sf_config.get('role', 'ACCOUNTADMIN')
            )
            self.cursor = self.conn.cursor()
            logger.info("✅ Connected to Snowflake successfully")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Snowflake: {e}")
            raise
    
    def execute_sql_file(self, sql_file_path: str):
        """Execute a SQL file"""
        sql_file = Path(sql_file_path)
        
        if not sql_file.exists():
            logger.error(f"SQL file not found: {sql_file}")
            return False
        
        logger.info(f"Executing SQL file: {sql_file.name}")
        
        try:
            with open(sql_file, 'r') as f:
                sql_content = f.read()
            
            # Split by semicolons and execute each statement
            statements = [s.strip() for s in sql_content.split(';') if s.strip()]
            
            for statement in statements:
                if statement and not statement.startswith('--'):
                    self.cursor.execute(statement)
            
            logger.info(f"✅ Successfully executed {sql_file.name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error executing {sql_file.name}: {e}")
            return False
    
    def create_tables(self):
        """Create all necessary tables"""
        sql_dir = Path(__file__).parent.parent.parent / "sql" / "ddl"
        
        files = [
            sql_dir / "presidents_dim.sql",
            sql_dir / "economic_facts.sql",
            sql_dir / "performance_view.sql"
        ]
        
        for sql_file in files:
            self.execute_sql_file(sql_file)
    
    def load_presidents_data(self, parquet_file: str):
        """Load presidents data from parquet file"""
        logger.info(f"Loading presidents data from {parquet_file}")
        
        try:
            df = pd.read_parquet(parquet_file)
            
            # Prepare data for Snowflake
            df['effective_date'] = datetime.now().date()
            df['expiration_date'] = None
            df['is_active'] = True
            df['created_at'] = datetime.now()
            df['updated_at'] = datetime.now()
            
            # Write to Snowflake
            from snowflake.connector.pandas_tools import write_pandas
            
            success, nchunks, nrows, _ = write_pandas(
                conn=self.conn,
                df=df,
                table_name='PRESIDENTS_DIM',
                database='SENEGAL_ANALYTICS',
                schema='PUBLIC',
                auto_create_table=False
            )
            
            if success:
                logger.info(f"✅ Loaded {nrows} presidents records")
                return True
            else:
                logger.error("❌ Failed to load presidents data")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error loading presidents data: {e}")
            return False
    
    def load_development_data(self, parquet_file: str):
        """Load World Bank development data from parquet file"""
        logger.info(f"Loading development data from {parquet_file}")
        
        try:
            df = pd.read_parquet(parquet_file)
            
            # Rename columns to match Snowflake schema
            df = df.rename(columns={
                'indicator_code': 'indicator_code',
                'indicator_name': 'indicator_name',
                'value': 'value',
                'year': 'year'
            })
            
            # Add required fields
            df['data_source'] = 'World Bank'
            df['is_estimated'] = False
            df['data_quality_score'] = 1.0
            df['country'] = 'Senegal'
            df['country_code'] = 'SN'
            df['created_at'] = datetime.now()
            df['updated_at'] = datetime.now()
            
            # Load presidents mapping to add president info
            presidents_df = self._get_president_mapping()
            if not presidents_df.empty:
                # Add president info based on year
                df = df.merge(
                    presidents_df[['year', 'president_id', 'president_name', 'party']],
                    on='year',
                    how='left'
                )
            
            # Select only columns that exist in target table
            columns_to_keep = [
                'year', 'indicator_code', 'indicator_name', 'value',
                'president_id', 'president_name', 'party',
                'country', 'country_code', 'data_source',
                'is_estimated', 'data_quality_score',
                'ingestion_timestamp', 'created_at', 'updated_at'
            ]
            
            df = df[[col for col in columns_to_keep if col in df.columns]]
            
            # Write to Snowflake
            from snowflake.connector.pandas_tools import write_pandas
            
            success, nchunks, nrows, _ = write_pandas(
                conn=self.conn,
                df=df,
                table_name='DEVELOPMENT_FACTS',
                database='SENEGAL_ANALYTICS',
                schema='PUBLIC',
                auto_create_table=False
            )
            
            if success:
                logger.info(f"✅ Loaded {nrows} development indicator records")
                return True
            else:
                logger.error("❌ Failed to load development data")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error loading development data: {e}")
            return False
    
    def _get_president_mapping(self) -> pd.DataFrame:
        """Get president to year mapping from Snowflake"""
        try:
            query = """
            SELECT 
                YEAR(dateadd(day, seq, start_date)) as year,
                president_id,
                president_name,
                party
            FROM presidents_dim,
            TABLE(FLATTEN(input => ARRAY_GENERATE_RANGE(0, DATEDIFF(day, start_date, COALESCE(end_date, CURRENT_DATE())))))
            WHERE is_active = TRUE
            """
            df = pd.read_sql(query, self.conn)
            return df
        except:
            return pd.DataFrame()
    
    def verify_data(self):
        """Verify loaded data"""
        logger.info("Verifying loaded data...")
        
        queries = {
            'Presidents': "SELECT COUNT(*) as count FROM presidents_dim WHERE is_active = TRUE",
            'Development Indicators': "SELECT COUNT(*) as count FROM development_facts",
            'Year Range': "SELECT MIN(year) as min_year, MAX(year) as max_year FROM development_facts",
            'Unique Indicators': "SELECT COUNT(DISTINCT indicator_code) as count FROM development_facts"
        }
        
        results = {}
        for name, query in queries.items():
            try:
                result = self.cursor.execute(query).fetchone()
                results[name] = result
                logger.info(f"{name}: {result}")
            except Exception as e:
                logger.error(f"Error checking {name}: {e}")
        
        return results
    
    def close(self):
        """Close Snowflake connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Snowflake connection closed")


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("🇸🇳 SENEGAL ANALYTICS - Snowflake Data Loader")
    print("="*70)
    
    loader = SnowflakeLoader()
    
    try:
        # Step 1: Create tables
        print("\n📋 Step 1: Creating tables...")
        loader.create_tables()
        
        # Step 2: Find latest data files
        data_dir = Path(__file__).parent.parent.parent / "data" / "raw"
        
        if not data_dir.exists():
            print("\n❌ Error: No data directory found!")
            print("Run data collection scripts first:")
            print("  python src/ingest/worldbank_api.py")
            print("  python src/ingest/presidents_data.py")
            return
        
        # Find latest files
        president_files = sorted(data_dir.glob("presidents_*.parquet"))
        worldbank_files = sorted(data_dir.glob("senegal_worldbank_*.parquet"))
        
        if not president_files or not worldbank_files:
            print("\n❌ Error: Data files not found!")
            print("Run data collection scripts first")
            return
        
        # Step 2: Load presidents
        print("\n👥 Step 2: Loading presidents data...")
        latest_presidents = president_files[-1]
        loader.load_presidents_data(latest_presidents)
        
        # Step 3: Load development data
        print("\n📊 Step 3: Loading development indicators...")
        latest_worldbank = worldbank_files[-1]
        loader.load_development_data(latest_worldbank)
        
        # Step 4: Verify
        print("\n✅ Step 4: Verifying data...")
        results = loader.verify_data()
        
        # Print summary
        print("\n" + "="*70)
        print("🎉 DATA LOAD COMPLETE!")
        print("="*70)
        print("\nYour Snowflake database is ready:")
        print("  Database: SENEGAL_ANALYTICS")
        print("  Tables: PRESIDENTS_DIM, DEVELOPMENT_FACTS")
        print("\nNext steps:")
        print("  1. Query your data in Snowflake")
        print("  2. Update dashboard to connect to Snowflake")
        print("  3. Run: streamlit run dashboard/app.py")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Load process failed: {e}")
    finally:
        loader.close()


if __name__ == "__main__":
    main()

