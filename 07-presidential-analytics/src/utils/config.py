"""
Configuration management for Presidential Analytics Pipeline
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration loader and manager"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            # Default to config.yaml in the config directory
            config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._load_env_overrides()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Config file not found: {self.config_path}\n"
                f"Please copy config.yaml.example to config.yaml and fill in your credentials"
            )
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_env_overrides(self):
        """Override config with environment variables if they exist"""
        # FRED API
        if os.getenv('FRED_API_KEY'):
            self.config['fred_api_key'] = os.getenv('FRED_API_KEY')
        
        # AWS
        if os.getenv('AWS_ACCESS_KEY_ID'):
            self.config['aws']['access_key_id'] = os.getenv('AWS_ACCESS_KEY_ID')
        if os.getenv('AWS_SECRET_ACCESS_KEY'):
            self.config['aws']['secret_access_key'] = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        # Snowflake
        if os.getenv('SNOWFLAKE_ACCOUNT'):
            self.config['snowflake']['account'] = os.getenv('SNOWFLAKE_ACCOUNT')
        if os.getenv('SNOWFLAKE_USER'):
            self.config['snowflake']['user'] = os.getenv('SNOWFLAKE_USER')
        if os.getenv('SNOWFLAKE_PASSWORD'):
            self.config['snowflake']['password'] = os.getenv('SNOWFLAKE_PASSWORD')
    
    def get(self, key: str, default=None):
        """Get configuration value by dot notation key (e.g., 'aws.region')"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    @property
    def fred_api_key(self) -> str:
        return self.config.get('fred_api_key')
    
    @property
    def aws_config(self) -> Dict[str, str]:
        return self.config.get('aws', {})
    
    @property
    def snowflake_config(self) -> Dict[str, str]:
        return self.config.get('snowflake', {})
    
    @property
    def fred_metrics(self) -> list:
        return self.config.get('data_collection', {}).get('fred_metrics', [])


# Singleton instance
_config_instance = None

def get_config() -> Config:
    """Get or create configuration singleton"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance

