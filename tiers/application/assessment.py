#!/usr/bin/env python3
"""
Application Security Assessment
Comprehensive security review for web applications and software systems
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any


class ApplicationSecurityAssessment:
    """Application security assessment for web applications and software systems"""
    
    def __init__(self):
        self.categories = {
            "authentication_authorization": {
                "name": "Authentication & Authorization",
                "description": "User authentication and access control mechanisms",
                "questions": [
                    "Is multi-factor authentication implemented and enforced?",
                    "Are password policies enforced (complexity, history, expiration)?",
                    "Is session management implemented securely?",
                    "Are authorization checks performed at all access points?",
                    "Is role-based access control (RBAC) implemented?",
                    "Are administrative functions properly protected?"
                ]
            },
            "input_validation": {
                "name": "Input Validation & Sanitization",
                "description": "Handling and validation of user inputs",
                "questions": [
                    "Is all user input validated on both client and server sides?",
                    "Are parameterized queries used to prevent SQL injection?",
                    "Is input sanitized to prevent XSS attacks?",
                    "Are file uploads validated and restricted?",
                    "Is input length and format validation implemented?",
                    "Are special characters properly handled and escaped?"
                ]
            },
            "data_protection": {
                "name": "Data Protection",
                "description": "Protection of sensitive data at rest and in transit",
                "questions": [
                    "Is sensitive data encrypted at rest using strong algorithms?",
                    "Is data encrypted in transit using TLS 1.2 or higher?",
                    "Are encryption keys properly managed and rotated?",
                    "Is personally identifiable information (PII) properly protected?",
                    "Are data retention and disposal policies implemented?",
                    "Is database access logged and monitored?"
                ]
            },
            "error_handling": {
                "name": "Error Handling & Logging",
                "description": "Secure error handling and comprehensive logging",
                "questions": [
                    "Are error messages generic and don't reveal system information?",
                    "Is comprehensive logging implemented for security events?",
                    "Are logs protected from unauthorized access and tampering?",
                    "Is log retention policy defined and implemented?",
                    "Are security events monitored and alerted?",
                    "Is exception handling implemented throughout the application?"
                ]
            },
            "session_management": {
                "name": "Session Management",
                "description": "Secure session handling and management",
                "questions": [
                    "Are session IDs generated using cryptographically secure methods?",
                    "Is session timeout implemented and appropriate?",
                    "Are sessions invalidated upon logout?",
                    "Is session fixation protection implemented?",
                    "Are session cookies secured with HttpOnly and Secure flags?",
                    "Is concurrent session control implemented where appropriate?"
                ]
            },
            "configuration_management": {
                "name": "Configuration Management",
                "description": "Secure configuration and deployment practices",
                "questions": [
                    "Are default credentials changed on all systems?",
                    "Is unnecessary functionality and services disabled?",
                    "Are security headers implemented (HSTS, CSP, etc.)?",
                    "Is the application deployed with minimal privileges?",
                    "Are configuration files secured and not publicly accessible?",
                    "Is the application hardened according to security standards?"
                ]
            },
            "api_security": {
                "name": "API Security",
                "description": "Security of application programming interfaces",
                "questions": [
                    "Is API authentication and authorization properly implemented?",
                    "Are API rate limiting and throttling mechanisms in place?",
                    "Is input validation implemented for all API endpoints?",
                    "Are API responses properly structured and validated?",
                    "Is API versioning and deprecation handled securely?",
                    "Are API security policies documented and enforced?"
                ]
            },
            "third_party_components": {
                "name": "Third-party Components",
                "description": "Security of external libraries and dependencies",
                "questions": [
                    "Are all third-party components inventoried and tracked?",
                    "Are components regularly updated to latest versions?",
                    "Are known vulnerabilities in components identified and patched?",
                    "Are unused components removed from the application?",
                    "Is there a process for evaluating new components?",
                    "Are component licenses reviewed for compliance?"
                ]
            },
            "business_logic": {
                "name": "Business Logic Security",
                "description": "Security of application-specific business logic",
                "questions": [
                    "Are business logic flaws and race conditions identified?",
                    "Is workflow validation implemented and enforced?",
                    "Are transaction limits and controls implemented?",
                    "Is data integrity validation performed?",
                    "Are business rule violations properly handled?",
                    "Is abuse case testing performed on critical functions?"
                ]
            },
            "deployment_environment": {
                "name": "Deployment Environment",
                "description": "Security of the deployment and runtime environment",
                "questions": [
                    "Is the production environment properly hardened?",
                    "Are development and testing environments secured?",
                    "Is network segmentation implemented?",
                    "Are security monitoring and alerting systems in place?",
                    "Is incident response plan specific to the application?",
                    "Are backups and disaster recovery procedures tested?"
                ]
            }
        }
        self.results = {}
    
    def conduct_assessment(self, application_name: str = "Unknown Application") -> Dict[str, Any]:
        """Conduct the application security assessment"""
        print(f"Application Security Assessment for: {application_name}")
        print("=" * 60)
        print("This assessment focuses on application-specific security controls")
        print("and development security practices.\n")
        
        self.results = {
            "application": application_name,
            "assessment_date": datetime.now().isoformat(),
            "tier": "Application Security",
            "categories": {},
            "overall_score": 0.0,
            "security_rating": "Unknown"
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
                score = self._calculate_question_score(response)
                
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
        
        # Calculate overall score and security rating
        self.results['overall_score'] = sum(category_scores) / len(category_scores)
        self.results['security_rating'] = self._determine_security_rating(self.results['overall_score'])
        
        return self.results
    
    def _simulate_response(self) -> str:
        """Simulate assessment responses for demonstration"""
        import random
        responses = [
            "Fully implemented with automated testing",
            "Implemented with manual verification",
            "Partially implemented",
            "Planned but not implemented",
            "Not implemented or unknown"
        ]
        return random.choice(responses)
    
    def _calculate_question_score(self, response: str) -> float:
        """Calculate numeric score from response"""
        response_lower = response.lower()
        if "fully implemented with automated" in response_lower:
            return 4.0
        elif "implemented with manual" in response_lower:
            return 3.0
        elif "partially implemented" in response_lower:
            return 2.0
        elif "planned but not" in response_lower:
            return 1.0
        else:
            return 0.0
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level based on score"""
        if score >= 3.5:
            return "Low Risk"
        elif score >= 2.5:
            return "Medium Risk"
        elif score >= 1.5:
            return "High Risk"
        else:
            return "Critical Risk"
    
    def _determine_security_rating(self, score: float) -> str:
        """Determine overall security rating based on score"""
        if score >= 3.5:
            return "Excellent"
        elif score >= 3.0:
            return "Good"
        elif score >= 2.0:
            return "Fair"
        elif score >= 1.0:
            return "Poor"
        else:
            return "Inadequate"
    
    def generate_remediation_plan(self) -> Dict[str, List[str]]:
        """Generate prioritized remediation plan"""
        if not self.results:
            return {}
        
        remediation_plan = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": []
        }
        
        for category_key, category in self.results['categories'].items():
            priority = "low"
            if category['risk_level'] == "Critical Risk":
                priority = "critical"
            elif category['risk_level'] == "High Risk":
                priority = "high"
            elif category['risk_level'] == "Medium Risk":
                priority = "medium"
            
            if priority in ["critical", "high"]:
                if category_key == "authentication_authorization":
                    remediation_plan[priority].extend([
                        "Implement multi-factor authentication",
                        "Enforce strong password policies",
                        "Review and strengthen authorization controls",
                        "Implement session management best practices"
                    ])
                elif category_key == "input_validation":
                    remediation_plan[priority].extend([
                        "Implement comprehensive input validation",
                        "Use parameterized queries for database access",
                        "Implement XSS prevention controls",
                        "Secure file upload functionality"
                    ])
                elif category_key == "data_protection":
                    remediation_plan[priority].extend([
                        "Implement encryption for sensitive data at rest",
                        "Enforce TLS 1.2+ for data in transit",
                        "Implement proper key management",
                        "Review and enhance data protection controls"
                    ])
                elif category_key == "session_management":
                    remediation_plan[priority].extend([
                        "Generate secure session identifiers",
                        "Implement proper session timeout",
                        "Secure session cookies with appropriate flags",
                        "Implement session fixation protection"
                    ])
                elif category_key == "configuration_management":
                    remediation_plan[priority].extend([
                        "Change all default credentials",
                        "Disable unnecessary services and functionality",
                        "Implement security headers",
                        "Harden application configuration"
                    ])
        
        # Add general recommendations based on overall security rating
        if self.results['security_rating'] in ["Poor", "Inadequate"]:
            remediation_plan["critical"].extend([
                "Conduct comprehensive security code review",
                "Perform penetration testing",
                "Implement security development lifecycle (SDL)",
                "Establish security testing in CI/CD pipeline"
            ])
        
        return remediation_plan
    
    def generate_owasp_top10_mapping(self) -> Dict[str, List[str]]:
        """Map findings to OWASP Top 10 vulnerabilities"""
        owasp_mapping = {
            "A01 - Broken Access Control": [],
            "A02 - Cryptographic Failures": [],
            "A03 - Injection": [],
            "A04 - Insecure Design": [],
            "A05 - Security Misconfiguration": [],
            "A06 - Vulnerable Components": [],
            "A07 - Identification and Authentication Failures": [],
            "A08 - Software and Data Integrity Failures": [],
            "A09 - Security Logging and Monitoring Failures": [],
            "A10 - Server-Side Request Forgery": []
        }
        
        for category_key, category in self.results['categories'].items():
            if category['risk_level'] in ["High Risk", "Critical Risk"]:
                if category_key == "authentication_authorization":
                    owasp_mapping["A01 - Broken Access Control"].append(category['name'])
                    owasp_mapping["A07 - Identification and Authentication Failures"].append(category['name'])
                elif category_key == "input_validation":
                    owasp_mapping["A03 - Injection"].append(category['name'])
                elif category_key == "data_protection":
                    owasp_mapping["A02 - Cryptographic Failures"].append(category['name'])
                elif category_key == "error_handling":
                    owasp_mapping["A09 - Security Logging and Monitoring Failures"].append(category['name'])
                elif category_key == "configuration_management":
                    owasp_mapping["A05 - Security Misconfiguration"].append(category['name'])
                elif category_key == "third_party_components":
                    owasp_mapping["A06 - Vulnerable Components"].append(category['name'])
                elif category_key == "business_logic":
                    owasp_mapping["A04 - Insecure Design"].append(category['name'])
        
        # Remove empty mappings
        return {k: v for k, v in owasp_mapping.items() if v}
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate assessment report"""
        if not self.results:
            raise ValueError("No assessment results available. Run conduct_assessment() first.")
        
        report = f"""
Application Security Assessment Report
====================================

Application: {self.results['application']}
Assessment Date: {self.results['assessment_date']}
Tier: {self.results['tier']}

Overall Security Rating: {self.results['security_rating']} ({self.results['overall_score']:.2f}/4.0)

Category Results:
"""
        
        for category_key, category in self.results['categories'].items():
            report += f"\n{category['name']}: {category['risk_level']} ({category['score']:.2f}/4.0)\n"
        
        # Add OWASP Top 10 mapping
        owasp_mapping = self.generate_owasp_top10_mapping()
        if owasp_mapping:
            report += "\nOWASP Top 10 Risk Mapping:\n"
            report += "-" * 25 + "\n"
            for owasp_item, categories in owasp_mapping.items():
                report += f"{owasp_item}: {', '.join(categories)}\n"
        
        # Add remediation plan
        remediation_plan = self.generate_remediation_plan()
        
        if remediation_plan["critical"]:
            report += "\nCritical Priority Remediation:\n"
            report += "-" * 30 + "\n"
            for i, item in enumerate(remediation_plan["critical"], 1):
                report += f"{i}. {item}\n"
        
        if remediation_plan["high"]:
            report += "\nHigh Priority Remediation:\n"
            report += "-" * 26 + "\n"
            for i, item in enumerate(remediation_plan["high"], 1):
                report += f"{i}. {item}\n"
        
        # Add testing recommendations
        report += "\nRecommended Security Testing:\n"
        report += "-" * 29 + "\n"
        if self.results['overall_score'] < 2.0:
            report += "1. Static Application Security Testing (SAST)\n"
            report += "2. Dynamic Application Security Testing (DAST)\n"
            report += "3. Interactive Application Security Testing (IAST)\n"
            report += "4. Manual penetration testing\n"
        else:
            report += "1. Regular automated security scanning\n"
            report += "2. Annual penetration testing\n"
            report += "3. Continuous security monitoring\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        
        return report
    
    def export_json(self, output_file: str):
        """Export results as JSON"""
        if not self.results:
            raise ValueError("No assessment results available. Run conduct_assessment() first.")
        
        # Add additional data to results before export
        self.results['remediation_plan'] = self.generate_remediation_plan()
        self.results['owasp_top10_mapping'] = self.generate_owasp_top10_mapping()
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results exported to: {output_file}")


def main():
    """Main function for command-line usage"""
    assessment = ApplicationSecurityAssessment()
    
    app_name = input("Enter application name (or press Enter for default): ").strip()
    if not app_name:
        app_name = "Unknown Application"
    
    print("\nStarting Application Security Assessment...")
    results = assessment.conduct_assessment(app_name)
    
    # Generate and save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"application_security_assessment_{timestamp}.txt"
    json_file = f"application_security_results_{timestamp}.json"
    
    report = assessment.generate_report(report_file)
    assessment.export_json(json_file)
    
    print("\n" + "="*60)
    print("ASSESSMENT COMPLETE")
    print(f"Report saved to: {report_file}")
    print(f"JSON results saved to: {json_file}")


if __name__ == "__main__":
    main()