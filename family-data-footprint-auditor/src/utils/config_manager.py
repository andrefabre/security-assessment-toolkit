#!/usr/bin/env python3
"""
Configuration Manager - Handles configuration loading and management
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages configuration for the family data footprint auditor"""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = {}
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file or create default"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self.logger.info(f"Configuration loaded from {self.config_path}")
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                self.config = self._get_default_config()
        else:
            self.logger.info("Config file not found, using defaults")
            self.config = self._get_default_config()
            self._save_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "assessment": {
                "timeout_seconds": 30,
                "max_retries": 3,
                "enable_social_media_audit": True,
                "enable_privacy_audit": True,
                "enable_exposure_audit": True
            },
            "social_media": {
                "platforms": [
                    "facebook", "instagram", "twitter", "linkedin", 
                    "tiktok", "snapchat", "youtube"
                ],
                "check_privacy_settings": True,
                "analyze_content": True,
                "risk_thresholds": {
                    "low": 3.0,
                    "medium": 6.0,
                    "high": 8.0
                }
            },
            "privacy": {
                "categories": [
                    "web_browsers", "email_services", "cloud_storage",
                    "search_engines", "mobile_apps", "smart_devices"
                ],
                "privacy_score_weights": {
                    "web_browsers": 0.2,
                    "email_services": 0.2,
                    "cloud_storage": 0.15,
                    "search_engines": 0.15,
                    "mobile_apps": 0.15,
                    "smart_devices": 0.15
                }
            },
            "data_exposure": {
                "check_types": [
                    "email_breaches", "social_media_leaks", "public_records",
                    "data_broker_sites", "government_databases", "professional_networks"
                ],
                "breach_apis": {
                    "haveibeenpwned": {
                        "enabled": False,
                        "api_key": ""
                    }
                },
                "exposure_thresholds": {
                    "low": 2.0,
                    "medium": 5.0,
                    "high": 7.0
                }
            },
            "reporting": {
                "formats": ["html", "json"],
                "include_charts": True,
                "include_recommendations": True,
                "output_directory": "./reports"
            },
            "age_groups": {
                "child": {
                    "max_age": 12,
                    "stricter_privacy": True,
                    "parental_controls": True
                },
                "teen": {
                    "max_age": 17,
                    "privacy_education": True,
                    "monitored_access": True
                },
                "adult": {
                    "full_assessment": True,
                    "professional_considerations": True
                }
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "family_auditor.log"
            }
        }
    
    def _save_default_config(self) -> None:
        """Save default configuration to file"""
        try:
            # Ensure config directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            
            self.logger.info(f"Default configuration saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Error saving default config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key"""
        keys = key.split('.')
        config_ref = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
        
        # Set the value
        config_ref[keys[-1]] = value
        
        # Save configuration
        self._save_config()
    
    def _save_config(self) -> None:
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            self.logger.debug("Configuration saved")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
    
    def get_social_media_platforms(self) -> list:
        """Get list of social media platforms to audit"""
        return self.get("social_media.platforms", [])
    
    def get_privacy_categories(self) -> list:
        """Get list of privacy categories to audit"""
        return self.get("privacy.categories", [])
    
    def get_exposure_check_types(self) -> list:
        """Get list of data exposure check types"""
        return self.get("data_exposure.check_types", [])
    
    def get_age_group_config(self, age_group: str) -> Dict[str, Any]:
        """Get configuration for specific age group"""
        return self.get(f"age_groups.{age_group}", {})
    
    def is_social_media_enabled(self) -> bool:
        """Check if social media auditing is enabled"""
        return self.get("assessment.enable_social_media_audit", True)
    
    def is_privacy_audit_enabled(self) -> bool:
        """Check if privacy auditing is enabled"""
        return self.get("assessment.enable_privacy_audit", True)
    
    def is_exposure_audit_enabled(self) -> bool:
        """Check if data exposure auditing is enabled"""
        return self.get("assessment.enable_exposure_audit", True)
    
    def get_timeout(self) -> int:
        """Get timeout for operations"""
        return self.get("assessment.timeout_seconds", 30)
    
    def get_max_retries(self) -> int:
        """Get maximum retries for operations"""
        return self.get("assessment.max_retries", 3)
    
    def get_output_directory(self) -> str:
        """Get output directory for reports"""
        return self.get("reporting.output_directory", "./reports")
    
    def get_report_formats(self) -> list:
        """Get list of report formats to generate"""
        return self.get("reporting.formats", ["html", "json"])
    
    def reload(self) -> None:
        """Reload configuration from file"""
        self._load_config()
        self.logger.info("Configuration reloaded")
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        try:
            # Check required sections
            required_sections = ["assessment", "social_media", "privacy", "data_exposure", "reporting"]
            for section in required_sections:
                if section not in self.config:
                    self.logger.error(f"Missing required configuration section: {section}")
                    return False
            
            # Validate timeout
            timeout = self.get("assessment.timeout_seconds")
            if not isinstance(timeout, int) or timeout <= 0:
                self.logger.error("Invalid timeout configuration")
                return False
            
            # Validate platforms list
            platforms = self.get("social_media.platforms")
            if not isinstance(platforms, list):
                self.logger.error("Social media platforms must be a list")
                return False
            
            # Validate output directory
            output_dir = self.get("reporting.output_directory")
            if not isinstance(output_dir, str):
                self.logger.error("Output directory must be a string")
                return False
            
            self.logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation error: {e}")
            return False