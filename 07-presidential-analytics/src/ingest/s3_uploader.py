"""
S3 Data Uploader
Uploads processed data files to AWS S3
"""
import boto3
from pathlib import Path
from datetime import datetime
from typing import List
import glob

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import get_config
from utils.logger import setup_logger

logger = setup_logger('s3_uploader')


class S3Uploader:
    """Upload data files to S3"""
    
    def __init__(self):
        self.config = get_config()
        aws_config = self.config.aws_config
        
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_config.get('access_key_id'),
            aws_secret_access_key=aws_config.get('secret_access_key'),
            region_name=aws_config.get('region', 'us-east-1')
        )
        
        self.bucket = aws_config.get('s3_bucket')
        self.prefix = aws_config.get('s3_prefix', 'presidential-data')
        
        logger.info(f"Initialized S3 uploader for bucket: {self.bucket}")
    
    def upload_file(self, local_path: str, s3_key: str = None) -> bool:
        """
        Upload a single file to S3
        
        Args:
            local_path: Path to local file
            s3_key: S3 object key (if None, uses filename)
        
        Returns:
            True if successful, False otherwise
        """
        local_path = Path(local_path)
        
        if not local_path.exists():
            logger.error(f"File not found: {local_path}")
            return False
        
        if s3_key is None:
            s3_key = f"{self.prefix}/{local_path.name}"
        
        try:
            logger.info(f"Uploading {local_path.name} to s3://{self.bucket}/{s3_key}")
            
            self.s3_client.upload_file(
                str(local_path),
                self.bucket,
                s3_key
            )
            
            logger.info(f"Successfully uploaded to S3: {s3_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            return False
    
    def upload_directory(self, local_dir: str, s3_prefix: str = None) -> dict:
        """
        Upload all files in a directory to S3
        
        Args:
            local_dir: Path to local directory
            s3_prefix: S3 prefix for uploaded files
        
        Returns:
            Dict with upload statistics
        """
        local_dir = Path(local_dir)
        
        if not local_dir.exists():
            logger.error(f"Directory not found: {local_dir}")
            return {'success': 0, 'failed': 0}
        
        if s3_prefix is None:
            s3_prefix = self.prefix
        
        files = list(local_dir.glob('*.parquet')) + list(local_dir.glob('*.csv'))
        
        stats = {'success': 0, 'failed': 0}
        
        for file_path in files:
            s3_key = f"{s3_prefix}/{file_path.name}"
            if self.upload_file(file_path, s3_key):
                stats['success'] += 1
            else:
                stats['failed'] += 1
        
        logger.info(f"Upload complete: {stats['success']} succeeded, {stats['failed']} failed")
        return stats
    
    def list_files(self, prefix: str = None) -> List[str]:
        """List files in S3 bucket"""
        if prefix is None:
            prefix = self.prefix
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix
            )
            
            files = [obj['Key'] for obj in response.get('Contents', [])]
            logger.info(f"Found {len(files)} files in s3://{self.bucket}/{prefix}")
            return files
            
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []
    
    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket)
            logger.info(f"Bucket {self.bucket} exists")
        except:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket)
                logger.info(f"Created bucket: {self.bucket}")
            except Exception as e:
                logger.error(f"Error creating bucket: {e}")


def main():
    """Main execution function"""
    logger.info("Starting S3 upload process")
    
    uploader = S3Uploader()
    
    # Ensure bucket exists
    uploader.create_bucket_if_not_exists()
    
    # Upload all raw data files
    data_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    
    if not data_dir.exists():
        logger.error(f"Data directory not found: {data_dir}")
        print("No data to upload. Run data ingestion scripts first.")
        return
    
    # Upload with raw prefix
    stats = uploader.upload_directory(data_dir, f"{uploader.prefix}/raw")
    
    # Print summary
    print("\n" + "="*60)
    print("S3 Upload Summary")
    print("="*60)
    print(f"Bucket: {uploader.bucket}")
    print(f"Prefix: {uploader.prefix}/raw")
    print(f"Files uploaded: {stats['success']}")
    print(f"Failed uploads: {stats['failed']}")
    print("="*60)
    
    # List uploaded files
    files = uploader.list_files(f"{uploader.prefix}/raw")
    if files:
        print("\nUploaded files:")
        for f in files[:10]:  # Show first 10
            print(f"  - {f}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more")
    
    logger.info("S3 upload process completed")


if __name__ == "__main__":
    main()

