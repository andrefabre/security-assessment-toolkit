#!/usr/bin/env python3
"""
Logger Setup - Configures logging for the family data footprint auditor
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logging(verbose: bool = False, log_file: str = None) -> None:
    """Setup logging configuration"""
    
    # Determine log level
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Create file handler if log file specified
    if log_file:
        try:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)  # Always log everything to file
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
        except Exception as e:
            logging.error(f"Failed to setup file logging: {e}")
    
    # Log startup message
    logging.info("Family Data Footprint Auditor - Logging initialized")
    if verbose:
        logging.debug("Verbose logging enabled")


def get_logger(name: str) -> logging.Logger:
    """Get logger for specific module"""
    return logging.getLogger(name)


def create_session_log_file() -> str:
    """Create a unique log file name for this session"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"logs/family_auditor_{timestamp}.log"