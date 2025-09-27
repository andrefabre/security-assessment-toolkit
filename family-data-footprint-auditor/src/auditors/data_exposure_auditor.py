#!/usr/bin/env python3
"""
Data Exposure Auditor - Checks for potential data leaks and exposures
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import random


class DataExposureAuditor:
    """Audits potential data exposures and leaks for family members"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Exposure check methods
        self.exposure_checks = {
            "email_breaches": self._check_email_breaches,
            "social_media_leaks": self._check_social_media_leaks,
            "public_records": self._check_public_records,
            "data_broker_sites": self._check_data_broker_sites,
            "government_databases": self._check_government_databases,
            "professional_networks": self._check_professional_networks
        }
    
    def audit_member(self, member_name: str, age_group: str) -> Dict[str, Any]:
        """Audit data exposure for a family member"""
        self.logger.info(f"Starting data exposure audit for: {member_name}")
        
        audit_results = {
            "member_name": member_name,
            "age_group": age_group,
            "audit_date": datetime.now().isoformat(),
            "exposure_checks": {},
            "overall_exposure_risk": 0.0,
            "critical_exposures": [],
            "exposed_data_types": [],
            "recommendations": []
        }
        
        # Run each exposure check
        for check_name, check_method in self.exposure_checks.items():
            try:
                check_results = check_method(member_name, age_group)
                audit_results["exposure_checks"][check_name] = check_results
            except Exception as e:
                self.logger.error(f"Error running {check_name} for {member_name}: {e}")
                audit_results["exposure_checks"][check_name] = {
                    "error": str(e),
                    "status": "check_failed"
                }
        
        # Calculate overall exposure risk
        audit_results["overall_exposure_risk"] = self._calculate_exposure_risk(
            audit_results["exposure_checks"]
        )
        
        # Identify critical exposures
        audit_results["critical_exposures"] = self._identify_critical_exposures(
            audit_results["exposure_checks"]
        )
        
        # Catalog exposed data types
        audit_results["exposed_data_types"] = self._catalog_exposed_data_types(
            audit_results["exposure_checks"]
        )
        
        # Generate recommendations
        audit_results["recommendations"] = self._generate_exposure_recommendations(
            audit_results["exposure_checks"], age_group
        )
        
        return audit_results
    
    def _check_email_breaches(self, member_name: str, age_group: str) -> Dict[str, Any]:
        """Check for email addresses in known data breaches"""
        # Simulated breach check results
        breach_count = random.randint(0, 5)
        breaches = []
        
        if breach_count > 0:
            potential_breaches = [
                {
                    "service": "LinkedIn",
                    "date": "2021-06-15",
                    "data_compromised": ["email", "password_hash", "profile_data"],
                    "severity": "high"
                },
                {
                    "service": "Adobe",
                    "date": "2013-10-03",
                    "data_compromised": ["email", "password", "username"],
                    "severity": "critical"
                },
                {
                    "service": "Dropbox",
                    "date": "2012-07-01",
                    "data_compromised": ["email", "password_hash"],
                    "severity": "medium"
                },
                {
                    "service": "Yahoo",
                    "date": "2014-09-01",
                    "data_compromised": ["email", "password", "security_questions", "phone"],
                    "severity": "critical"
                },
                {
                    "service": "Facebook",
                    "date": "2019-04-03",
                    "data_compromised": ["email", "phone", "profile_data"],
                    "severity": "high"
                }
            ]
            breaches = random.sample(potential_breaches, min(breach_count, len(potential_breaches)))
        
        return {
            "check_type": "Email Breaches",
            "emails_checked": 2,  # Primary and secondary email
            "breaches_found": len(breaches),
            "breach_details": breaches,
            "risk_score": min(len(breaches) * 2.0, 10.0),
            "last_checked": datetime.now().isoformat(),
            "recommendations": [
                "Change passwords for affected accounts",
                "Enable two-factor authentication",
                "Monitor accounts for suspicious activity",
                "Consider using unique passwords for each service"
            ] if breaches else ["Continue monitoring for new breaches"]
        }
    
    def _check_social_media_leaks(self, member_name: str, age_group: str) -> Dict[str, Any]:
        """Check for social media data leaks"""
        # Simulated social media leak check
        leak_risk = random.choice(["low", "medium", "high"])
        
        leaks_found = []
        if leak_risk in ["medium", "high"]:
            potential_leaks = [
                {
                    "platform": "Instagram",
                    "leak_type": "scraped_profiles",
                    "data_exposed": ["username", "bio", "follower_count", "photos"],
                    "date_discovered": "2023-03-15",
                    "severity": "medium"
                },
                {
                    "platform": "Twitter",
                    "leak_type": "api_abuse",
                    "data_exposed": ["username", "tweets", "followers", "location_data"],
                    "date_discovered": "2023-01-10",
                    "severity": "high"
                }
            ]
            leak_count = 1 if leak_risk == "medium" else 2
            leaks_found = random.sample(potential_leaks, leak_count)
        
        return {
            "check_type": "Social Media Leaks",
            "platforms_checked": ["Facebook", "Instagram", "Twitter", "LinkedIn", "TikTok"],
            "leaks_found": len(leaks_found),
            "leak_details": leaks_found,
            "risk_score": {"low": 2.0, "medium": 5.0, "high": 8.0}[leak_risk],
            "recommendations": [
                "Review privacy settings on all social platforms",
                "Limit personal information in public profiles",
                "Regularly audit follower/friend lists",
                "Consider making accounts private"
            ] if leaks_found else ["Continue monitoring social media privacy settings"]
        }
    
    def _check_public_records(self, member_name: str, age_group: str) -> Dict[str, Any]:
        """Check for information in public records"""
        if age_group in ["child", "teen"]:
            return {
                "check_type": "Public Records",
                "records_found": 0,
                "note": "Limited public records expected for minors",
                "risk_score": 0.0
            }
        
        # Simulated public records check
        record_types = []
        risk_score = 0.0
        
        if random.choice([True, False]):  # 50% chance of finding records
            potential_records = [
                {
                    "type": "property_records",
                    "data_exposed": ["name", "address", "property_value"],
                    "source": "county_assessor",
                    "privacy_risk": "medium"
                },
                {
                    "type": "voter_registration",
                    "data_exposed": ["name", "address", "age", "party_affiliation"],
                    "source": "election_office",
                    "privacy_risk": "low"
                },
                {
                    "type": "business_registration", 
                    "data_exposed": ["name", "business_address", "role"],
                    "source": "secretary_of_state",
                    "privacy_risk": "low"
                },
                {
                    "type": "court_records",
                    "data_exposed": ["name", "case_details", "addresses"],
                    "source": "court_system",
                    "privacy_risk": "high"
                }
            ]
            record_count = random.randint(1, 3)
            record_types = random.sample(potential_records, record_count)
            risk_score = sum({"low": 1.0, "medium": 3.0, "high": 6.0}[r["privacy_risk"]] for r in record_types)
        
        return {
            "check_type": "Public Records",
            "records_found": len(record_types),
            "record_details": record_types,
            "risk_score": min(risk_score, 10.0),
            "recommendations": [
                "Request removal from public databases where possible",
                "Opt out of data broker sites",
                "Monitor public records for accuracy",
                "Consider using a P.O. Box for public filings"
            ] if record_types else ["Continue monitoring public record exposure"]
        }
    
    def _check_data_broker_sites(self, member_name: str, age_group: str) -> Dict[str, Any]:
        """Check for information on data broker websites"""
        # Simulated data broker check
        broker_listings = []
        
        if random.choice([True, True, False]):  # 66% chance of finding listings
            potential_brokers = [
                {
                    "broker": "WhitePages",
                    "data_found": ["name", "address", "phone", "age", "relatives"],
                    "removal_possible": True,
                    "privacy_risk": "high"
                },
                {
                    "broker": "Spokeo",
                    "data_found": ["name", "address", "phone", "email", "social_profiles"],
                    "removal_possible": True,
                    "privacy_risk": "high"
                },
                {
                    "broker": "BeenVerified",
                    "data_found": ["name", "address", "background_info", "relatives"],
                    "removal_possible": True,
                    "privacy_risk": "medium"
                },
                {
                    "broker": "PeopleFinder",
                    "data_found": ["name", "address", "phone", "property_records"],
                    "removal_possible": False,
                    "privacy_risk": "medium"
                }
            ]
            listing_count = random.randint(1, 4)
            broker_listings = random.sample(potential_brokers, listing_count)
        
        risk_score = sum({"medium": 3.0, "high": 5.0}[b["privacy_risk"]] for b in broker_listings)
        
        return {
            "check_type": "Data Broker Sites",
            "brokers_checked": 15,
            "listings_found": len(broker_listings),
            "broker_details": broker_listings,
            "removable_listings": len([b for b in broker_listings if b["removal_possible"]]),
            "risk_score": min(risk_score, 10.0),
            "recommendations": [
                "Submit removal requests to data brokers",
                "Use opt-out services to remove from multiple sites",
                "Regularly monitor for new listings",
                "Consider using privacy protection services"
            ] if broker_listings else ["Continue periodic monitoring of data broker sites"]
        }
    
    def _check_government_databases(self, member_name: str, age_group: str) -> Dict[str, Any]:
        """Check for information in government databases"""
        # Simulated government database check
        database_exposure = random.choice(["none", "minimal", "moderate"])
        
        exposures = []
        if database_exposure != "none":
            potential_exposures = [
                {
                    "database": "professional_licenses",
                    "data_exposed": ["name", "license_number", "address", "discipline_records"],
                    "agency": "state_licensing_board",
                    "privacy_risk": "medium"
                },
                {
                    "database": "campaign_contributions",
                    "data_exposed": ["name", "address", "employer", "contribution_amount"],
                    "agency": "election_commission", 
                    "privacy_risk": "low"
                },
                {
                    "database": "environmental_permits",
                    "data_exposed": ["name", "business_address", "permit_details"],
                    "agency": "environmental_protection",
                    "privacy_risk": "low"
                }
            ]
            exposure_count = 1 if database_exposure == "minimal" else 2
            exposures = random.sample(potential_exposures, exposure_count)
        
        risk_score = sum({"low": 1.0, "medium": 3.0}[e["privacy_risk"]] for e in exposures)
        
        return {
            "check_type": "Government Databases",
            "databases_checked": 8,
            "exposures_found": len(exposures),
            "exposure_details": exposures,
            "risk_score": min(risk_score, 10.0),
            "recommendations": [
                "Review what information is required to be public",
                "Request corrections for inaccurate information",
                "Understand your rights regarding government data",
                "Consider privacy implications before public filings"
            ] if exposures else ["Government database exposure is minimal"]
        }
    
    def _check_professional_networks(self, member_name: str, age_group: str) -> Dict[str, Any]:
        """Check for professional network exposures"""
        if age_group in ["child", "teen"]:
            return {
                "check_type": "Professional Networks",
                "networks_checked": 0,
                "note": "Professional networks not applicable for age group",
                "risk_score": 0.0
            }
        
        # Simulated professional network check
        network_exposure = random.choice(["minimal", "moderate", "extensive"])
        
        exposures = {
            "linkedin": {
                "profile_public": True,
                "contact_info_visible": network_exposure in ["moderate", "extensive"],
                "employment_history": True,
                "connections_visible": network_exposure == "extensive",
                "activity_visible": network_exposure == "extensive"
            },
            "professional_directories": {
                "industry_listings": network_exposure in ["moderate", "extensive"],
                "conference_attendee_lists": network_exposure == "extensive",
                "professional_certifications": True
            }
        }
        
        risk_mapping = {"minimal": 2.0, "moderate": 5.0, "extensive": 8.0}
        
        return {
            "check_type": "Professional Networks",
            "networks_checked": ["LinkedIn", "Industry Directories", "Professional Associations"],
            "exposure_level": network_exposure,
            "exposure_details": exposures,
            "risk_score": risk_mapping[network_exposure],
            "recommendations": [
                "Review LinkedIn privacy settings",
                "Limit contact information visibility",
                "Consider who can see your connections",
                "Be selective about professional information shared",
                "Regularly audit professional profiles"
            ]
        }
    
    def _calculate_exposure_risk(self, exposure_checks: Dict[str, Any]) -> float:
        """Calculate overall data exposure risk"""
        total_risk = 0.0
        check_count = 0
        
        for check_data in exposure_checks.values():
            if "risk_score" in check_data:
                total_risk += check_data["risk_score"]
                check_count += 1
        
        return total_risk / check_count if check_count > 0 else 0.0
    
    def _identify_critical_exposures(self, exposure_checks: Dict[str, Any]) -> List[str]:
        """Identify critical data exposures requiring immediate attention"""
        critical_exposures = []
        
        for check_data in exposure_checks.values():
            if "risk_score" in check_data and check_data["risk_score"] >= 7.0:
                check_type = check_data.get("check_type", "Unknown")
                critical_exposures.append(f"High risk exposure in {check_type}")
                
                # Add specific details for critical exposures
                if "breach_details" in check_data:
                    for breach in check_data["breach_details"]:
                        if breach.get("severity") == "critical":
                            critical_exposures.append(f"Critical breach: {breach['service']}")
                
                if "leak_details" in check_data:
                    for leak in check_data["leak_details"]:
                        if leak.get("severity") == "high":
                            critical_exposures.append(f"High severity leak: {leak['platform']}")
        
        return critical_exposures
    
    def _catalog_exposed_data_types(self, exposure_checks: Dict[str, Any]) -> List[str]:
        """Catalog all types of data that have been exposed"""
        exposed_data = set()
        
        for check_data in exposure_checks.values():
            # Check breach details
            if "breach_details" in check_data:
                for breach in check_data["breach_details"]:
                    exposed_data.update(breach.get("data_compromised", []))
            
            # Check leak details
            if "leak_details" in check_data:
                for leak in check_data["leak_details"]:
                    exposed_data.update(leak.get("data_exposed", []))
            
            # Check record details
            if "record_details" in check_data:
                for record in check_data["record_details"]:
                    exposed_data.update(record.get("data_exposed", []))
            
            # Check broker details
            if "broker_details" in check_data:
                for broker in check_data["broker_details"]:
                    exposed_data.update(broker.get("data_found", []))
        
        return list(exposed_data)
    
    def _generate_exposure_recommendations(self, exposure_checks: Dict[str, Any], age_group: str) -> List[str]:
        """Generate recommendations to reduce data exposure"""
        recommendations = set()
        
        # Collect recommendations from each check
        for check_data in exposure_checks.values():
            if "recommendations" in check_data:
                recommendations.update(check_data["recommendations"])
        
        # Add age-specific recommendations
        if age_group in ["child", "teen"]:
            recommendations.update([
                "Monitor child's digital footprint regularly",
                "Educate about long-term implications of online activity",
                "Use parental controls to limit data exposure",
                "Be cautious about sharing personal information online"
            ])
        
        # Add general high-priority recommendations
        recommendations.update([
            "Implement a regular data exposure monitoring routine",
            "Use identity monitoring services",
            "Create alerts for your name and personal information",
            "Practice good data hygiene and minimize information sharing",
            "Review and update privacy settings regularly"
        ])
        
        return list(recommendations)