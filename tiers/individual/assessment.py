#!/usr/bin/env python3
"""
Individual Tier Security Assessment
Tailored security assessment for individual users and home environments
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any


class IndividualTierAssessment:
    """Individual/Home user security assessment"""
    
    def __init__(self):
        self.categories = {
            "device_security": {
                "name": "Device Security",
                "description": "Security of personal devices (computers, phones, tablets)",
                "questions": [
                    "Are all devices protected with strong passwords/PINs?",
                    "Do you keep your operating systems and software updated?",
                    "Do you use antivirus software on your computers?",
                    "Are automatic security updates enabled?",
                    "Do you use device encryption (BitLocker, FileVault, etc.)?"
                ]
            },
            "network_security": {
                "name": "Network Security",
                "description": "Home network and Wi-Fi security",
                "questions": [
                    "Is your Wi-Fi network secured with WPA3 or WPA2?",
                    "Have you changed default router passwords?",
                    "Do you use a strong, unique Wi-Fi password?",
                    "Is guest network enabled for visitors?",
                    "Do you regularly update your router firmware?"
                ]
            },
            "password_management": {
                "name": "Password Management",
                "description": "Password security and management practices",
                "questions": [
                    "Do you use unique passwords for each account?",
                    "Do you use a password manager?",
                    "Are your passwords strong (12+ characters, complex)?",
                    "Do you enable two-factor authentication where available?",
                    "Do you avoid sharing passwords with others?"
                ]
            },
            "data_protection": {
                "name": "Data Protection",
                "description": "Personal data backup and protection",
                "questions": [
                    "Do you regularly backup important files?",
                    "Are your backups stored in multiple locations?",
                    "Do you test your backup restoration process?",
                    "Is sensitive data encrypted?",
                    "Do you securely dispose of old devices and media?"
                ]
            },
            "online_behavior": {
                "name": "Online Behavior",
                "description": "Safe internet and email practices",
                "questions": [
                    "Do you verify website URLs before entering credentials?",
                    "Do you avoid clicking suspicious links in emails?",
                    "Do you verify sender identity before opening attachments?",
                    "Do you use secure, HTTPS websites for sensitive activities?",
                    "Do you review privacy settings on social media?"
                ]
            },
            "software_management": {
                "name": "Software Management",
                "description": "Software installation and management practices",
                "questions": [
                    "Do you only install software from trusted sources?",
                    "Do you review permissions before installing apps?",
                    "Do you uninstall software you no longer use?",
                    "Do you avoid pirated or cracked software?",
                    "Do you keep software licenses up to date?"
                ]
            }
        }
        self.results = {}
    
    def conduct_assessment(self, user_name: str = "Unknown User") -> Dict[str, Any]:
        """Conduct the individual tier assessment"""
        print(f"Individual Tier Security Assessment for: {user_name}")
        print("=" * 60)
        print("This assessment focuses on personal cybersecurity practices")
        print("and home environment security.\n")
        
        self.results = {
            "user": user_name,
            "assessment_date": datetime.now().isoformat(),
            "tier": "Individual",
            "categories": {},
            "overall_score": 0.0
        }
        
        category_scores = []
        
        for category_key, category in self.categories.items():
            print(f"\n{category['name']}")
            print("-" * len(category['name']))
            print(f"Description: {category['description']}")
            
            category_results = {
                "name": category['name'],
                "description": category['description'],
                "responses": {},
                "score": 0.0,
                "risk_level": "Unknown"
            }
            
            question_scores = []
            
            for i, question in enumerate(category['questions']):
                print(f"\nQ{i+1}: {question}")
                
                # Simulate response (in real implementation, this would be interactive)
                response = self._simulate_response()
                score = 1 if response.lower().startswith('y') else 0
                
                category_results['responses'][f"q{i+1}"] = {
                    "question": question,
                    "answer": response,
                    "score": score
                }
                question_scores.append(score)
            
            # Calculate category score and risk level
            category_score = sum(question_scores) / len(question_scores)
            category_results['score'] = category_score
            category_results['risk_level'] = self._determine_risk_level(category_score)
            
            self.results['categories'][category_key] = category_results
            category_scores.append(category_score)
        
        # Calculate overall score
        self.results['overall_score'] = sum(category_scores) / len(category_scores)
        
        return self.results
    
    def _simulate_response(self) -> str:
        """Simulate assessment responses for demonstration"""
        import random
        responses = ["Yes", "No", "Sometimes", "Not sure"]
        return random.choice(responses)
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level based on score"""
        if score >= 0.8:
            return "Low Risk"
        elif score >= 0.6:
            return "Medium Risk"
        elif score >= 0.4:
            return "High Risk"
        else:
            return "Critical Risk"
    
    def generate_recommendations(self) -> List[str]:
        """Generate personalized security recommendations"""
        if not self.results:
            return []
        
        recommendations = []
        
        for category_key, category in self.results['categories'].items():
            if category['score'] < 0.6:  # High or Critical risk
                if category_key == "device_security":
                    recommendations.extend([
                        "Enable automatic security updates on all devices",
                        "Install reputable antivirus software",
                        "Use strong, unique passwords for device logins",
                        "Enable device encryption (BitLocker/FileVault)"
                    ])
                elif category_key == "network_security":
                    recommendations.extend([
                        "Upgrade to WPA3 wireless security",
                        "Change default router admin passwords",
                        "Enable guest network for visitors",
                        "Update router firmware regularly"
                    ])
                elif category_key == "password_management":
                    recommendations.extend([
                        "Install and use a password manager",
                        "Enable two-factor authentication on all important accounts",
                        "Create unique passwords for each account",
                        "Use passwords with at least 12 characters"
                    ])
                elif category_key == "data_protection":
                    recommendations.extend([
                        "Set up automatic backups to cloud and external drive",
                        "Test backup restoration monthly",
                        "Encrypt sensitive files and folders",
                        "Securely wipe old devices before disposal"
                    ])
                elif category_key == "online_behavior":
                    recommendations.extend([
                        "Always verify URLs before entering credentials",
                        "Be cautious with email attachments from unknown senders",
                        "Use secure (HTTPS) websites for sensitive activities",
                        "Review and update social media privacy settings"
                    ])
                elif category_key == "software_management":
                    recommendations.extend([
                        "Only install software from official app stores or websites",
                        "Review app permissions before installation",
                        "Regularly uninstall unused software",
                        "Avoid pirated or cracked software"
                    ])
        
        # Add general recommendations based on overall score
        if self.results['overall_score'] < 0.5:
            recommendations.extend([
                "Consider taking a basic cybersecurity awareness course",
                "Schedule monthly security check-ups",
                "Create an incident response plan for personal use"
            ])
        
        return list(set(recommendations))  # Remove duplicates
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate assessment report"""
        if not self.results:
            raise ValueError("No assessment results available. Run conduct_assessment() first.")
        
        overall_risk = self._determine_risk_level(self.results['overall_score'])
        
        report = f"""
Individual Tier Security Assessment Report
========================================

User: {self.results['user']}
Assessment Date: {self.results['assessment_date']}
Tier: {self.results['tier']}

Overall Security Score: {self.results['overall_score']:.2f}/1.0 ({overall_risk})

Category Results:
"""
        
        for category_key, category in self.results['categories'].items():
            report += f"\n{category['name']}: {category['score']:.2f}/1.0 ({category['risk_level']})\n"
        
        # Add recommendations
        recommendations = self.generate_recommendations()
        if recommendations:
            report += "\nPersonalized Security Recommendations:\n"
            report += "-" * 38 + "\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"{i}. {rec}\n"
        
        # Add next steps
        report += "\nNext Steps:\n"
        report += "-" * 11 + "\n"
        if overall_risk in ["High Risk", "Critical Risk"]:
            report += "1. Address high-priority recommendations immediately\n"
            report += "2. Implement basic security measures within 1 week\n"
            report += "3. Schedule follow-up assessment in 1 month\n"
        else:
            report += "1. Implement remaining recommendations\n"
            report += "2. Schedule follow-up assessment in 3 months\n"
            report += "3. Stay informed about new security threats\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        
        return report
    
    def export_json(self, output_file: str):
        """Export results as JSON"""
        if not self.results:
            raise ValueError("No assessment results available. Run conduct_assessment() first.")
        
        # Add recommendations to results before export
        self.results['recommendations'] = self.generate_recommendations()
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results exported to: {output_file}")


def main():
    """Main function for command-line usage"""
    assessment = IndividualTierAssessment()
    
    user_name = input("Enter your name (or press Enter for default): ").strip()
    if not user_name:
        user_name = "Unknown User"
    
    print("\nStarting Individual Tier Security Assessment...")
    results = assessment.conduct_assessment(user_name)
    
    # Generate and save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"individual_assessment_{timestamp}.txt"
    json_file = f"individual_results_{timestamp}.json"
    
    report = assessment.generate_report(report_file)
    assessment.export_json(json_file)
    
    print("\n" + "="*60)
    print("ASSESSMENT COMPLETE")
    print(f"Report saved to: {report_file}")
    print(f"JSON results saved to: {json_file}")


if __name__ == "__main__":
    main()