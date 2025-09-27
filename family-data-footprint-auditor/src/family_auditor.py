#!/usr/bin/env python3
"""
Family Data Auditor - Main orchestration class for family digital footprint assessment
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from .auditors.social_media_auditor import SocialMediaAuditor
from .auditors.privacy_settings_auditor import PrivacySettingsAuditor
from .auditors.data_exposure_auditor import DataExposureAuditor
from .analyzers.footprint_analyzer import FootprintAnalyzer
from .reports.family_report_generator import FamilyReportGenerator
from .utils.config_manager import ConfigManager


class FamilyDataAuditor:
    """Main orchestration class for family data footprint auditing"""
    
    def __init__(self, family_name: str, config_path: str, output_dir: str):
        self.family_name = family_name
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir)
        self.family_members = []
        self.results = {}
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = ConfigManager(config_path)
        
        # Initialize auditors
        self.social_media_auditor = SocialMediaAuditor(self.config)
        self.privacy_auditor = PrivacySettingsAuditor(self.config)
        self.data_exposure_auditor = DataExposureAuditor(self.config)
        
        # Initialize analyzer and report generator
        self.analyzer = FootprintAnalyzer(self.config)
        self.report_generator = FamilyReportGenerator(self.config)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def add_family_member(self, member_name: str, age_group: str = "adult") -> None:
        """Add a family member to the assessment"""
        member = {
            "name": member_name,
            "age_group": age_group,
            "added_at": datetime.now().isoformat()
        }
        self.family_members.append(member)
        self.logger.info(f"Added family member: {member_name}")
    
    def run_assessment(self) -> Dict[str, Any]:
        """Run the complete family data footprint assessment"""
        self.logger.info(f"Starting assessment for family: {self.family_name}")
        
        # Initialize results structure
        self.results = {
            "family_name": self.family_name,
            "assessment_date": datetime.now().isoformat(),
            "family_members": self.family_members,
            "individual_results": {},
            "family_summary": {},
            "recommendations": []
        }
        
        # Run assessment for each family member
        for member in self.family_members:
            member_name = member["name"]
            self.logger.info(f"Assessing family member: {member_name}")
            
            member_results = self._assess_individual_member(member)
            self.results["individual_results"][member_name] = member_results
        
        # Analyze family-wide patterns
        self.results["family_summary"] = self.analyzer.analyze_family_patterns(
            self.results["individual_results"]
        )
        
        # Generate recommendations
        self.results["recommendations"] = self.analyzer.generate_family_recommendations(
            self.results
        )
        
        # Generate reports
        report_path = self._generate_reports()
        self.results["report_path"] = str(report_path)
        
        return self.results
    
    def _assess_individual_member(self, member: Dict[str, Any]) -> Dict[str, Any]:
        """Assess an individual family member's digital footprint"""
        member_name = member["name"]
        age_group = member.get("age_group", "adult")
        
        member_results = {
            "name": member_name,
            "age_group": age_group,
            "social_media": {},
            "privacy_settings": {},
            "data_exposure": {},
            "risk_score": 0.0,
            "recommendations": []
        }
        
        try:
            # Social media footprint analysis
            member_results["social_media"] = self.social_media_auditor.audit_member(
                member_name, age_group
            )
            
            # Privacy settings audit
            member_results["privacy_settings"] = self.privacy_auditor.audit_member(
                member_name, age_group
            )
            
            # Data exposure check
            member_results["data_exposure"] = self.data_exposure_auditor.audit_member(
                member_name, age_group
            )
            
            # Calculate individual risk score
            member_results["risk_score"] = self.analyzer.calculate_individual_risk(
                member_results
            )
            
            # Generate individual recommendations
            member_results["recommendations"] = self.analyzer.generate_individual_recommendations(
                member_results
            )
            
        except Exception as e:
            self.logger.error(f"Error assessing {member_name}: {e}")
            member_results["error"] = str(e)
        
        return member_results
    
    def _generate_reports(self) -> Path:
        """Generate assessment reports"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate main family report
        report_filename = f"family_footprint_report_{timestamp}.html"
        report_path = self.output_dir / report_filename
        
        self.report_generator.generate_family_report(
            self.results,
            str(report_path)
        )
        
        # Generate JSON data export
        json_filename = f"family_footprint_data_{timestamp}.json"
        json_path = self.output_dir / json_filename
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Generate individual member reports
        for member_name, member_results in self.results["individual_results"].items():
            member_report_filename = f"{member_name.lower().replace(' ', '_')}_report_{timestamp}.html"
            member_report_path = self.output_dir / member_report_filename
            
            self.report_generator.generate_individual_report(
                member_results,
                str(member_report_path)
            )
        
        self.logger.info(f"Reports generated in: {self.output_dir}")
        return report_path
    
    def save_results(self, filepath: Optional[str] = None) -> str:
        """Save assessment results to JSON file"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.output_dir / f"family_assessment_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        return str(filepath)