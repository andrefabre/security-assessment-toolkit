#!/usr/bin/env python3
"""
Family Data Footprint Auditor
Main entry point for the family digital footprint assessment tool
"""

import argparse
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.family_auditor import FamilyDataAuditor
from src.utils.logger import setup_logging


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="Family Data Footprint Auditor - Assess family digital security"
    )
    
    parser.add_argument(
        "--family-name",
        type=str,
        help="Family name for the assessment",
        default="Unknown Family"
    )
    
    parser.add_argument(
        "--member",
        type=str,
        action="append",
        help="Add a family member to assess (can be used multiple times)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for reports",
        default="./reports"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Configuration file path",
        default="./config/default.json"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    
    # Initialize the family auditor
    auditor = FamilyDataAuditor(
        family_name=args.family_name,
        config_path=args.config,
        output_dir=args.output_dir
    )
    
    # Add family members if specified
    if args.member:
        for member in args.member:
            auditor.add_family_member(member)
    
    # Run the assessment
    try:
        print(f"Starting Family Data Footprint Assessment for: {args.family_name}")
        results = auditor.run_assessment()
        
        print("\nAssessment completed successfully!")
        print(f"Results saved to: {results['report_path']}")
        
    except Exception as e:
        print(f"Error during assessment: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()