from os import environ as env
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass

class Config:
    """Configuration manager for the application.
    
    This class handles loading and managing configuration from environment variables
    and YAML configuration files.
    """
    
    API_KEY: Optional[str] = env.get("API_KEY")
    CHROMA_PATH: Optional[str] = env.get("CHROMA_PATH")
    DATA_PATH: Optional[str] = env.get("DATA_PATH")
    CONFIG_PATH: Optional[str] = env.get("CONFIG_FILE")
    SECRET_PATH: str = env.get("SECRET_FILE")


    @classmethod
    def load_config(cls, type:str) -> Dict[str, Any]:
        """Load configuration from the YAML file specified in CONFIG_FILE.
        
        Returns:
            Dict[str, Any]: The loaded configuration as a dictionary.
            
        Raises:
            ConfigError: If the configuration file is not found or cannot be loaded.
            yaml.YAMLError: If the YAML file is invalid.
        """
        path = cls.CONFIG_PATH
        if type == "secret":
            path = cls.SECRET_PATH

        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if not isinstance(config, dict):
                    raise ConfigError("Configuration file must contain a dictionary")
                return config
        except yaml.YAMLError as e:
            raise ConfigError(f"Error parsing YAML configuration: {str(e)}")
        except Exception as e:
            raise ConfigError(f"Error loading configuration: {str(e)}")

    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """Get database configuration from the loaded config.
        
        Returns:
            Dict[str, Any]: Database configuration dictionary.
            
        Raises:
            ConfigError: If database configuration is missing or invalid.
        """
        config = cls.load_config("config")
        if 'database' not in config:
            raise ConfigError("Database configuration not found in config file")
        return config['database']
    
    @classmethod
    def get_secret_config(cls) -> str:
        """Get secret configuration from the loaded config.
        
        Returns:
            str: Secret configuration dictionary.
            
        Raises:
            ConfigError: If secret configuration is missing or invalid.
        """
        config = cls.load_config()
        if 'jwt_secret_key' not in config:
            raise ConfigError("Secret configuration not found in config file")
        return config['jwt_secret_key']