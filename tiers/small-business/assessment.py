#!/usr/bin/env python3
"""
Small Business Tier Security Assessment
Tailored security assessment for small businesses and organizations
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any


class SmallBusinessAssessment:
    """Small business security assessment"""
    
    def __init__(self):
        self.categories = {
            "access_management": {
                "name": "Access Management",
                "description": "User accounts, authentication, and access controls",
                "questions": [
                    "Are unique user accounts created for each employee?",
                    "Is multi-factor authentication enforced for all users?",
                    "Are administrative privileges limited to necessary personnel?",
                    "Is there a formal process for onboarding/offboarding employees?",
                    "Are user access rights reviewed regularly?",
                    "Do you maintain an inventory of all user accounts?"
                ]
            },
            "network_security": {
                "name": "Network Security",
                "description": "Network infrastructure and perimeter security",
                "questions": [
                    "Is a business-grade firewall deployed and configured?",
                    "Are network devices secured with strong passwords?",
                    "Is network segmentation implemented where appropriate?",
                    "Are wireless networks secured with WPA3/WPA2-Enterprise?",
                    "Is remote access secured with VPN?",
                    "Are network vulnerabilities scanned regularly?"
                ]
            },
            "endpoint_security": {
                "name": "Endpoint Security",
                "description": "Security of employee devices and workstations",
                "questions": [
                    "Is enterprise antivirus/anti-malware deployed on all devices?",
                    "Are operating systems and software kept updated?",
                    "Is device encryption enforced on all business devices?",
                    "Are mobile devices managed through MDM/EMM solution?",
                    "Is USB and removable media usage controlled?",
                    "Are security policies enforced on all endpoints?"
                ]
            },
            "data_protection": {
                "name": "Data Protection",
                "description": "Data backup, encryption, and privacy controls",
                "questions": [
                    "Are regular, automated backups performed for critical data?",
                    "Are backups stored both on-site and off-site?",
                    "Is backup restoration tested regularly?",
                    "Is sensitive data encrypted at rest and in transit?",
                    "Are data retention and disposal policies in place?",
                    "Is customer/client data properly protected?"
                ]
            },
            "incident_response": {
                "name": "Incident Response",
                "description": "Security incident handling and business continuity",
                "questions": [
                    "Is there a formal incident response plan?",
                    "Are employees trained on incident reporting procedures?",
                    "Are security incidents logged and tracked?",
                    "Is there a business continuity/disaster recovery plan?",
                    "Are incident response procedures tested regularly?",
                    "Are external incident response contacts established?"
                ]
            },
            "security_awareness": {
                "name": "Security Awareness",
                "description": "Employee training and security culture",
                "questions": [
                    "Do employees receive regular security awareness training?",
                    "Is phishing simulation training conducted?",
                    "Are security policies documented and communicated?",
                    "Is there a process for reporting security concerns?",
                    "Are security responsibilities clearly defined?",
                    "Is security performance measured and tracked?"
                ]
            },
            "vendor_management": {
                "name": "Vendor Management",
                "description": "Third-party and supply chain security",
                "questions": [
                    "Are vendor security assessments conducted?",
                    "Are contracts with security requirements in place?",
                    "Is third-party access monitored and controlled?",
                    "Are vendor security incidents reported and tracked?",
                    "Is there a process for vendor risk assessment?",
                    "Are critical vendor dependencies identified?"
                ]
            },
            "compliance_governance": {
                "name": "Compliance & Governance",
                "description": "Regulatory compliance and security governance",
                "questions": [
                    "Are applicable regulations and standards identified?",
                    "Is compliance status regularly assessed?",
                    "Are security policies reviewed and updated annually?",
                    "Is there executive oversight of cybersecurity?",
                    "Are security metrics reported to management?",
                    "Is cybersecurity included in business planning?"
                ]
            }
        }
        self.results = {}
    
    def conduct_assessment(self, business_name: str = "Unknown Business") -> Dict[str, Any]:
        """Conduct the small business tier assessment"""
        print(f"Small Business Tier Security Assessment for: {business_name}")
        print("=" * 60)
        print("This assessment focuses on organizational cybersecurity practices")
        print("and business environment security.\n")
        
        self.results = {
            "business": business_name,
            "assessment_date": datetime.now().isoformat(),
            "tier": "Small Business",
            "categories": {},
            "overall_score": 0.0,
            "maturity_level": "Basic"
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
                "maturity": "Basic"
            }
            
            question_scores = []
            
            for i, question in enumerate(category['questions']):
                print(f"\nQ{i+1}: {question}")
                
                # Simulate response (in real implementation, this would be interactive)
                response = self._simulate_response()
                score = self._calculate_question_score(response)
                
                category_results['responses'][f"q{i+1}"] = {
                    "question": question,
                    "answer": response,
                    "score": score
                }
                question_scores.append(score)
            
            # Calculate category score and maturity level
            category_score = sum(question_scores) / len(question_scores)
            category_results['score'] = category_score
            category_results['maturity'] = self._determine_maturity(category_score)
            
            self.results['categories'][category_key] = category_results
            category_scores.append(category_score)
        
        # Calculate overall score and maturity
        self.results['overall_score'] = sum(category_scores) / len(category_scores)
        self.results['maturity_level'] = self._determine_maturity(self.results['overall_score'])
        
        return self.results
    
    def _simulate_response(self) -> str:
        """Simulate assessment responses for demonstration"""
        import random
        responses = [
            "Fully implemented with regular review",
            "Implemented but needs improvement",
            "Partially implemented",
            "Planning to implement",
            "Not implemented"
        ]
        return random.choice(responses)
    
    def _calculate_question_score(self, response: str) -> float:
        """Calculate numeric score from response"""
        response_lower = response.lower()
        if "fully implemented" in response_lower:
            return 4.0
        elif "implemented but needs" in response_lower:
            return 3.0
        elif "partially implemented" in response_lower:
            return 2.0
        elif "planning to implement" in response_lower:
            return 1.0
        else:
            return 0.0
    
    def _determine_maturity(self, score: float) -> str:
        """Determine maturity level based on score"""
        if score >= 3.5:
            return "Advanced"
        elif score >= 2.5:
            return "Intermediate"
        elif score >= 1.5:
            return "Developing"
        else:
            return "Basic"
    
    def generate_action_plan(self) -> Dict[str, List[str]]:
        """Generate prioritized action plan"""
        if not self.results:
            return {}
        
        action_plan = {
            "immediate": [],
            "short_term": [],
            "long_term": []
        }
        
        # Immediate actions (score < 1.5)
        for category_key, category in self.results['categories'].items():
            if category['score'] < 1.5:
                if category_key == "access_management":
                    action_plan["immediate"].extend([
                        "Implement multi-factor authentication for all users",
                        "Create unique accounts for each employee",
                        "Remove unnecessary administrative privileges"
                    ])
                elif category_key == "network_security":
                    action_plan["immediate"].extend([
                        "Deploy and configure business-grade firewall",
                        "Secure wireless networks with WPA3/WPA2-Enterprise",
                        "Change default passwords on all network devices"
                    ])
                elif category_key == "endpoint_security":
                    action_plan["immediate"].extend([
                        "Deploy enterprise antivirus on all devices",
                        "Enable automatic security updates",
                        "Implement device encryption"
                    ])
                elif category_key == "data_protection":
                    action_plan["immediate"].extend([
                        "Set up automated daily backups",
                        "Test backup restoration process",
                        "Implement data encryption for sensitive information"
                    ])
        
        # Short-term actions (score 1.5-2.5)
        for category_key, category in self.results['categories'].items():
            if 1.5 <= category['score'] < 2.5:
                if category_key == "incident_response":
                    action_plan["short_term"].extend([
                        "Develop formal incident response plan",
                        "Train employees on incident reporting",
                        "Establish external incident response contacts"
                    ])
                elif category_key == "security_awareness":
                    action_plan["short_term"].extend([
                        "Implement regular security training program",
                        "Conduct phishing simulation exercises",
                        "Document and communicate security policies"
                    ])
                elif category_key == "vendor_management":
                    action_plan["short_term"].extend([
                        "Conduct security assessments of key vendors",
                        "Include security requirements in vendor contracts",
                        "Monitor and control third-party access"
                    ])
        
        # Long-term actions (score 2.5-3.5)
        for category_key, category in self.results['categories'].items():
            if 2.5 <= category['score'] < 3.5:
                action_plan["long_term"].extend([
                    f"Enhance {category['name'].lower()} capabilities",
                    f"Implement advanced {category['name'].lower()} controls",
                    f"Regular review and improvement of {category['name'].lower()}"
                ])
        
        # General recommendations based on overall maturity
        if self.results['maturity_level'] == "Basic":
            action_plan["immediate"].extend([
                "Engage cybersecurity consultant for assessment",
                "Establish cybersecurity budget and resources",
                "Assign cybersecurity responsibilities"
            ])
        
        return action_plan
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate assessment report"""
        if not self.results:
            raise ValueError("No assessment results available. Run conduct_assessment() first.")
        
        report = f"""
Small Business Tier Security Assessment Report
============================================

Business: {self.results['business']}
Assessment Date: {self.results['assessment_date']}
Tier: {self.results['tier']}

Overall Security Maturity: {self.results['maturity_level']} ({self.results['overall_score']:.2f}/4.0)

Category Results:
"""
        
        for category_key, category in self.results['categories'].items():
            report += f"\n{category['name']}: {category['maturity']} ({category['score']:.2f}/4.0)\n"
        
        # Add action plan
        action_plan = self.generate_action_plan()
        
        if action_plan["immediate"]:
            report += "\nImmediate Actions (0-30 days):\n"
            report += "-" * 30 + "\n"
            for i, action in enumerate(action_plan["immediate"], 1):
                report += f"{i}. {action}\n"
        
        if action_plan["short_term"]:
            report += "\nShort-term Actions (1-6 months):\n"
            report += "-" * 32 + "\n"
            for i, action in enumerate(action_plan["short_term"], 1):
                report += f"{i}. {action}\n"
        
        if action_plan["long_term"]:
            report += "\nLong-term Actions (6-12 months):\n"
            report += "-" * 31 + "\n"
            for i, action in enumerate(action_plan["long_term"], 1):
                report += f"{i}. {action}\n"
        
        # Add compliance considerations
        report += "\nCompliance Considerations:\n"
        report += "-" * 25 + "\n"
        if self.results['overall_score'] < 2.0:
            report += "- Focus on basic security hygiene before compliance\n"
            report += "- Consider cyber insurance requirements\n"
        else:
            report += "- Review industry-specific compliance requirements\n"
            report += "- Consider formal security certifications\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        
        return report
    
    def export_json(self, output_file: str):
        """Export results as JSON"""
        if not self.results:
            raise ValueError("No assessment results available. Run conduct_assessment() first.")
        
        # Add action plan to results before export
        self.results['action_plan'] = self.generate_action_plan()
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results exported to: {output_file}")


def main():
    """Main function for command-line usage"""
    assessment = SmallBusinessAssessment()
    
    business_name = input("Enter business name (or press Enter for default): ").strip()
    if not business_name:
        business_name = "Unknown Business"
    
    print("\nStarting Small Business Tier Security Assessment...")
    results = assessment.conduct_assessment(business_name)
    
    # Generate and save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"small_business_assessment_{timestamp}.txt"
    json_file = f"small_business_results_{timestamp}.json"
    
    report = assessment.generate_report(report_file)
    assessment.export_json(json_file)
    
    print("\n" + "="*60)
    print("ASSESSMENT COMPLETE")
    print(f"Report saved to: {report_file}")
    print(f"JSON results saved to: {json_file}")


if __name__ == "__main__":
    main()