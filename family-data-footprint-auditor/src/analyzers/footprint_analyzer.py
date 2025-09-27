#!/usr/bin/env python3
"""
Footprint Analyzer - Analyzes digital footprint data and generates insights
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import statistics


class FootprintAnalyzer:
    """Analyzes family digital footprint data and generates insights"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
    
    def analyze_family_patterns(self, individual_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns across family members"""
        self.logger.info("Analyzing family-wide digital footprint patterns")
        
        family_analysis = {
            "total_members": len(individual_results),
            "age_group_distribution": self._analyze_age_groups(individual_results),
            "risk_score_analysis": self._analyze_risk_scores(individual_results),
            "common_vulnerabilities": self._identify_common_vulnerabilities(individual_results),
            "platform_usage_patterns": self._analyze_platform_usage(individual_results),
            "privacy_maturity_levels": self._analyze_privacy_maturity(individual_results),
            "family_risk_profile": self._generate_family_risk_profile(individual_results),
            "improvement_priorities": self._identify_improvement_priorities(individual_results)
        }
        
        return family_analysis
    
    def calculate_individual_risk(self, member_results: Dict[str, Any]) -> float:
        """Calculate individual risk score from assessment results"""
        risk_components = []
        
        # Social media risk
        if "social_media" in member_results and "overall_risk_score" in member_results["social_media"]:
            risk_components.append(member_results["social_media"]["overall_risk_score"])
        
        # Privacy settings risk (invert privacy score since higher privacy = lower risk)
        if "privacy_settings" in member_results and "overall_privacy_score" in member_results["privacy_settings"]:
            privacy_score = member_results["privacy_settings"]["overall_privacy_score"]
            privacy_risk = 10.0 - privacy_score  # Invert: high privacy = low risk
            risk_components.append(privacy_risk)
        
        # Data exposure risk
        if "data_exposure" in member_results and "overall_exposure_risk" in member_results["data_exposure"]:
            risk_components.append(member_results["data_exposure"]["overall_exposure_risk"])
        
        # Calculate weighted average
        if risk_components:
            return sum(risk_components) / len(risk_components)
        else:
            return 5.0  # Default moderate risk if no data
    
    def generate_individual_recommendations(self, member_results: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations for an individual"""
        recommendations = set()
        
        # Collect recommendations from each assessment category
        for category in ["social_media", "privacy_settings", "data_exposure"]:
            if category in member_results and "recommendations" in member_results[category]:
                recommendations.update(member_results[category]["recommendations"])
        
        # Add risk-based recommendations
        risk_score = member_results.get("risk_score", 5.0)
        age_group = member_results.get("age_group", "adult")
        
        if risk_score >= 7.0:
            recommendations.update([
                "URGENT: Address high-risk exposures immediately",
                "Consider professional privacy consultation",
                "Implement comprehensive digital cleanup plan"
            ])
        elif risk_score >= 5.0:
            recommendations.update([
                "Prioritize privacy settings improvements",
                "Implement regular security check routine",
                "Consider identity monitoring services"
            ])
        
        # Age-specific recommendations
        if age_group in ["child", "teen"]:
            recommendations.update([
                "Increase parental monitoring and guidance",
                "Focus on digital literacy education",
                "Implement age-appropriate privacy controls"
            ])
        
        return list(recommendations)
    
    def generate_family_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate family-wide recommendations"""
        family_recommendations = []
        
        family_summary = results.get("family_summary", {})
        
        # Risk-based recommendations
        family_risk = family_summary.get("family_risk_profile", {}).get("overall_risk", 5.0)
        
        if family_risk >= 7.0:
            family_recommendations.extend([
                "FAMILY PRIORITY: Conduct comprehensive digital security overhaul",
                "Schedule family digital security meeting",
                "Consider professional cybersecurity consultation",
                "Implement family-wide password manager",
                "Create family digital emergency response plan"
            ])
        elif family_risk >= 5.0:
            family_recommendations.extend([
                "Establish regular family digital security reviews",
                "Implement shared security best practices",
                "Create family privacy guidelines"
            ])
        
        # Age-based recommendations
        age_groups = family_summary.get("age_group_distribution", {})
        if age_groups.get("child", 0) > 0 or age_groups.get("teen", 0) > 0:
            family_recommendations.extend([
                "Establish family digital safety rules",
                "Implement parental controls across devices",
                "Schedule regular digital literacy education",
                "Create safe communication channels for reporting issues"
            ])
        
        # Platform-specific recommendations
        common_vulnerabilities = family_summary.get("common_vulnerabilities", [])
        if "social_media_privacy" in common_vulnerabilities:
            family_recommendations.append("Family-wide social media privacy settings review needed")
        if "weak_passwords" in common_vulnerabilities:
            family_recommendations.append("Implement family password manager and training")
        if "data_exposure" in common_vulnerabilities:
            family_recommendations.append("Conduct family data exposure cleanup campaign")
        
        return family_recommendations
    
    def _analyze_age_groups(self, individual_results: Dict[str, Any]) -> Dict[str, int]:
        """Analyze age group distribution in family"""
        age_groups = {}
        
        for member_data in individual_results.values():
            age_group = member_data.get("age_group", "adult")
            age_groups[age_group] = age_groups.get(age_group, 0) + 1
        
        return age_groups
    
    def _analyze_risk_scores(self, individual_results: Dict[str, Any]) -> Dict[str, float]:
        """Analyze risk score distribution"""
        risk_scores = []
        
        for member_data in individual_results.values():
            if "risk_score" in member_data:
                risk_scores.append(member_data["risk_score"])
        
        if not risk_scores:
            return {"average": 5.0, "min": 5.0, "max": 5.0, "median": 5.0}
        
        return {
            "average": statistics.mean(risk_scores),
            "min": min(risk_scores),
            "max": max(risk_scores),
            "median": statistics.median(risk_scores),
            "high_risk_members": len([score for score in risk_scores if score >= 7.0]),
            "low_risk_members": len([score for score in risk_scores if score <= 3.0])
        }
    
    def _identify_common_vulnerabilities(self, individual_results: Dict[str, Any]) -> List[str]:
        """Identify vulnerabilities common across family members"""
        vulnerability_patterns = {}
        
        for member_data in individual_results.values():
            # Check social media risks
            if "social_media" in member_data:
                for platform_data in member_data["social_media"].get("platforms", {}).values():
                    for risk in platform_data.get("risk_indicators", []):
                        key = f"social_media_{risk.lower().replace(' ', '_')}"
                        vulnerability_patterns[key] = vulnerability_patterns.get(key, 0) + 1
            
            # Check privacy issues
            if "privacy_settings" in member_data:
                for issue in member_data["privacy_settings"].get("critical_issues", []):
                    key = f"privacy_{issue.lower().replace(' ', '_')}"
                    vulnerability_patterns[key] = vulnerability_patterns.get(key, 0) + 1
            
            # Check data exposure
            if "data_exposure" in member_data:
                for exposure in member_data["data_exposure"].get("critical_exposures", []):
                    key = f"exposure_{exposure.lower().replace(' ', '_')}"
                    vulnerability_patterns[key] = vulnerability_patterns.get(key, 0) + 1
        
        # Return vulnerabilities affecting multiple family members
        family_size = len(individual_results)
        threshold = max(1, family_size // 2)  # At least half the family
        
        common_vulnerabilities = [
            vuln for vuln, count in vulnerability_patterns.items() 
            if count >= threshold
        ]
        
        return common_vulnerabilities
    
    def _analyze_platform_usage(self, individual_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze platform usage patterns across family"""
        platform_usage = {}
        total_members = len(individual_results)
        
        for member_data in individual_results.values():
            if "social_media" in member_data:
                for platform_name, platform_data in member_data["social_media"].get("platforms", {}).items():
                    if platform_data.get("account_found", False):
                        if platform_name not in platform_usage:
                            platform_usage[platform_name] = {
                                "users": 0,
                                "total_risk_score": 0.0,
                                "high_risk_users": 0
                            }
                        
                        platform_usage[platform_name]["users"] += 1
                        risk_score = platform_data.get("risk_score", 5.0)
                        platform_usage[platform_name]["total_risk_score"] += risk_score
                        
                        if risk_score >= 7.0:
                            platform_usage[platform_name]["high_risk_users"] += 1
        
        # Calculate usage statistics
        for platform_name, data in platform_usage.items():
            data["usage_percentage"] = (data["users"] / total_members) * 100
            data["average_risk_score"] = data["total_risk_score"] / data["users"]
            data["high_risk_percentage"] = (data["high_risk_users"] / data["users"]) * 100
        
        return platform_usage
    
    def _analyze_privacy_maturity(self, individual_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze privacy maturity levels across family members"""
        privacy_scores = []
        maturity_levels = {"basic": 0, "developing": 0, "intermediate": 0, "advanced": 0}
        
        for member_data in individual_results.values():
            if "privacy_settings" in member_data:
                privacy_score = member_data["privacy_settings"].get("overall_privacy_score", 5.0)
                privacy_scores.append(privacy_score)
                
                # Categorize maturity level
                if privacy_score >= 8.0:
                    maturity_levels["advanced"] += 1
                elif privacy_score >= 6.0:
                    maturity_levels["intermediate"] += 1
                elif privacy_score >= 4.0:
                    maturity_levels["developing"] += 1
                else:
                    maturity_levels["basic"] += 1
        
        return {
            "average_privacy_score": statistics.mean(privacy_scores) if privacy_scores else 5.0,
            "maturity_distribution": maturity_levels,
            "family_privacy_level": self._determine_family_privacy_level(maturity_levels)
        }
    
    def _generate_family_risk_profile(self, individual_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall family risk profile"""
        risk_scores = []
        high_risk_members = []
        
        for member_name, member_data in individual_results.items():
            risk_score = member_data.get("risk_score", 5.0)
            risk_scores.append(risk_score)
            
            if risk_score >= 7.0:
                high_risk_members.append({
                    "name": member_name,
                    "risk_score": risk_score,
                    "age_group": member_data.get("age_group", "adult")
                })
        
        overall_risk = statistics.mean(risk_scores) if risk_scores else 5.0
        
        # Determine risk level
        if overall_risk >= 7.0:
            risk_level = "High"
        elif overall_risk >= 5.0:
            risk_level = "Medium"
        elif overall_risk >= 3.0:
            risk_level = "Low"
        else:
            risk_level = "Very Low"
        
        return {
            "overall_risk": overall_risk,
            "risk_level": risk_level,
            "high_risk_members": high_risk_members,
            "risk_distribution": {
                "high": len([s for s in risk_scores if s >= 7.0]),
                "medium": len([s for s in risk_scores if 4.0 <= s < 7.0]),
                "low": len([s for s in risk_scores if s < 4.0])
            }
        }
    
    def _identify_improvement_priorities(self, individual_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify improvement priorities for the family"""
        priority_areas = []
        
        # Analyze common high-risk areas
        risk_areas = {
            "social_media_privacy": 0,
            "data_exposure": 0,
            "password_security": 0,
            "device_security": 0,
            "online_behavior": 0
        }
        
        family_size = len(individual_results)
        
        for member_data in individual_results.values():
            # Check social media risks
            if "social_media" in member_data:
                social_risk = member_data["social_media"].get("overall_risk_score", 5.0)
                if social_risk >= 6.0:
                    risk_areas["social_media_privacy"] += 1
            
            # Check data exposure
            if "data_exposure" in member_data:
                exposure_risk = member_data["data_exposure"].get("overall_exposure_risk", 5.0)
                if exposure_risk >= 6.0:
                    risk_areas["data_exposure"] += 1
            
            # Check privacy settings
            if "privacy_settings" in member_data:
                privacy_score = member_data["privacy_settings"].get("overall_privacy_score", 5.0)
                if privacy_score <= 4.0:  # Low privacy score = high risk
                    risk_areas["password_security"] += 1
                    risk_areas["device_security"] += 1
        
        # Create priority list
        for area, affected_members in risk_areas.items():
            if affected_members > 0:
                priority_level = "High" if affected_members >= family_size * 0.6 else "Medium"
                priority_areas.append({
                    "area": area,
                    "affected_members": affected_members,
                    "priority_level": priority_level,
                    "percentage_affected": (affected_members / family_size) * 100
                })
        
        # Sort by number of affected members (descending)
        priority_areas.sort(key=lambda x: x["affected_members"], reverse=True)
        
        return priority_areas
    
    def _determine_family_privacy_level(self, maturity_levels: Dict[str, int]) -> str:
        """Determine overall family privacy maturity level"""
        total_members = sum(maturity_levels.values())
        
        if total_members == 0:
            return "Unknown"
        
        # Calculate weighted score
        weights = {"basic": 1, "developing": 2, "intermediate": 3, "advanced": 4}
        weighted_score = sum(count * weights[level] for level, count in maturity_levels.items())
        average_score = weighted_score / total_members
        
        if average_score >= 3.5:
            return "Advanced"
        elif average_score >= 2.5:
            return "Intermediate"
        elif average_score >= 1.5:
            return "Developing"
        else:
            return "Basic"