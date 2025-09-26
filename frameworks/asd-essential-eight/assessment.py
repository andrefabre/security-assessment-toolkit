#!/usr/bin/env python3
"""
ASD Essential Eight Security Assessment Framework
Implements the Australian Signals Directorate (ASD) Essential Eight cybersecurity strategies
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any


class EssentialEightAssessment:
    """ASD Essential Eight assessment implementation"""
    
    def __init__(self):
        self.strategies = {
            "application_control": {
                "name": "Application Control",
                "description": "Application control prevents execution of unapproved/malicious programs",
                "maturity_levels": ["ML1", "ML2", "ML3"],
                "questions": [
                    "Are application control rules configured to prevent execution of executables, software libraries, scripts, installers, compiled HTML, HTML applications and control panel applets?",
                    "Is application control implemented using application whitelisting?",
                    "Are application control rules regularly updated?"
                ]
            },
            "patch_applications": {
                "name": "Patch Applications",
                "description": "Security vulnerabilities in applications are patched regularly",
                "maturity_levels": ["ML1", "ML2", "ML3"],
                "questions": [
                    "Are security vulnerabilities in applications patched within two weeks of release?",
                    "Is an automated method of asset discovery used?",
                    "Are patches tested before deployment?"
                ]
            },
            "configure_microsoft_office_macro_settings": {
                "name": "Configure Microsoft Office Macro Settings",
                "description": "Microsoft Office macros are disabled or restricted",
                "maturity_levels": ["ML1", "ML2", "ML3"],
                "questions": [
                    "Are Microsoft Office macros disabled for users that do not need them?",
                    "Are macros only allowed to execute from trusted locations?",
                    "Are antivirus scanning enabled for macros?"
                ]
            },
            "user_application_hardening": {
                "name": "User Application Hardening",
                "description": "Web browsers and PDF viewers are configured securely",
                "maturity_levels": ["ML1", "ML2", "ML3"],
                "questions": [
                    "Are web browsers configured to block Java, Flash, and untrusted JavaScript?",
                    "Are PDF viewers configured to disable JavaScript?",
                    "Are web advertisements blocked?"
                ]
            },
            "restrict_administrative_privileges": {
                "name": "Restrict Administrative Privileges",
                "description": "Administrative privileges are restricted and monitored",
                "maturity_levels": ["ML1", "ML2", "ML3"],
                "questions": [
                    "Are administrative privileges restricted to only those who need them?",
                    "Are privileged accounts used only for administrative tasks?",
                    "Are administrative activities logged and monitored?"
                ]
            },
            "patch_operating_systems": {
                "name": "Patch Operating Systems",
                "description": "Operating systems are kept up to date with security patches",
                "maturity_levels": ["ML1", "ML2", "ML3"],
                "questions": [
                    "Are operating system security vulnerabilities patched within one month?",
                    "Is an automated method used to confirm and record patching?",
                    "Are patches tested before deployment to production systems?"
                ]
            },
            "multi_factor_authentication": {
                "name": "Multi-factor Authentication",
                "description": "Multi-factor authentication is used to control access",
                "maturity_levels": ["ML1", "ML2", "ML3"],
                "questions": [
                    "Is multi-factor authentication used for all users?",
                    "Is multi-factor authentication used for all privileged accounts?",
                    "Are hardware tokens or software tokens used for authentication?"
                ]
            },
            "regular_backups": {
                "name": "Regular Backups",
                "description": "Important data is backed up regularly and restoration tested",
                "maturity_levels": ["ML1", "ML2", "ML3"],
                "questions": [
                    "Are backups performed regularly for important data?",
                    "Are backup restoration processes tested regularly?",
                    "Are backups stored offline or in an immutable state?"
                ]
            }
        }
        self.results = {}
    
    def conduct_assessment(self, organization_name: str = "Unknown Organization") -> Dict[str, Any]:
        """Conduct the Essential Eight assessment"""
        print(f"ASD Essential Eight Security Assessment for: {organization_name}")
        print("=" * 60)
        
        self.results = {
            "organization": organization_name,
            "assessment_date": datetime.now().isoformat(),
            "framework": "ASD Essential Eight",
            "strategies": {}
        }
        
        for strategy_key, strategy in self.strategies.items():
            print(f"\n{strategy['name']}")
            print("-" * len(strategy['name']))
            print(f"Description: {strategy['description']}")
            
            strategy_results = {
                "name": strategy['name'],
                "description": strategy['description'],
                "responses": {},
                "maturity_level": "ML0",
                "recommendations": []
            }
            
            for i, question in enumerate(strategy['questions']):
                print(f"\nQ{i+1}: {question}")
                
                # In a real implementation, this would be interactive
                # For now, we'll simulate responses
                response = self._simulate_response()
                strategy_results['responses'][f"q{i+1}"] = {
                    "question": question,
                    "answer": response,
                    "score": 1 if response.lower().startswith('y') else 0
                }
            
            # Calculate maturity level based on responses
            total_score = sum(r['score'] for r in strategy_results['responses'].values())
            total_questions = len(strategy['questions'])
            
            if total_score == total_questions:
                strategy_results['maturity_level'] = "ML3"
            elif total_score >= total_questions * 0.7:
                strategy_results['maturity_level'] = "ML2"
            elif total_score >= total_questions * 0.4:
                strategy_results['maturity_level'] = "ML1"
            else:
                strategy_results['maturity_level'] = "ML0"
            
            # Add recommendations based on maturity level
            if strategy_results['maturity_level'] in ["ML0", "ML1"]:
                strategy_results['recommendations'].append(f"Implement basic {strategy['name'].lower()} controls")
            if strategy_results['maturity_level'] in ["ML0", "ML1", "ML2"]:
                strategy_results['recommendations'].append(f"Enhance {strategy['name'].lower()} monitoring and automation")
            
            self.results['strategies'][strategy_key] = strategy_results
        
        return self.results
    
    def _simulate_response(self) -> str:
        """Simulate assessment responses for demonstration"""
        import random
        responses = ["Yes, fully implemented", "Partially implemented", "No, not implemented"]
        return random.choice(responses)
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate assessment report"""
        if not self.results:
            raise ValueError("No assessment results available. Run conduct_assessment() first.")
        
        report = f"""
ASD Essential Eight Security Assessment Report
============================================

Organization: {self.results['organization']}
Assessment Date: {self.results['assessment_date']}
Framework: {self.results['framework']}

Executive Summary:
"""
        
        # Calculate overall maturity
        maturity_scores = {"ML0": 0, "ML1": 1, "ML2": 2, "ML3": 3}
        avg_maturity = sum(maturity_scores[s['maturity_level']] for s in self.results['strategies'].values()) / len(self.results['strategies'])
        
        if avg_maturity >= 2.5:
            overall_maturity = "ML3 - Advanced"
        elif avg_maturity >= 1.5:
            overall_maturity = "ML2 - Intermediate"
        elif avg_maturity >= 0.5:
            overall_maturity = "ML1 - Basic"
        else:
            overall_maturity = "ML0 - Inadequate"
        
        report += f"Overall Maturity Level: {overall_maturity}\n\n"
        
        report += "Strategy Assessment Results:\n"
        report += "-" * 30 + "\n"
        
        for strategy_key, strategy in self.results['strategies'].items():
            report += f"\n{strategy['name']}: {strategy['maturity_level']}\n"
            if strategy['recommendations']:
                report += "Recommendations:\n"
                for rec in strategy['recommendations']:
                    report += f"  - {rec}\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        
        return report
    
    def export_json(self, output_file: str):
        """Export results as JSON"""
        if not self.results:
            raise ValueError("No assessment results available. Run conduct_assessment() first.")
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results exported to: {output_file}")


def main():
    """Main function for command-line usage"""
    assessment = EssentialEightAssessment()
    
    org_name = input("Enter organization name (or press Enter for default): ").strip()
    if not org_name:
        org_name = "Unknown Organization"
    
    print("\nStarting ASD Essential Eight Assessment...")
    results = assessment.conduct_assessment(org_name)
    
    # Generate and save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"essential_eight_report_{timestamp}.txt"
    json_file = f"essential_eight_results_{timestamp}.json"
    
    report = assessment.generate_report(report_file)
    assessment.export_json(json_file)
    
    print("\n" + "="*60)
    print("ASSESSMENT COMPLETE")
    print(f"Report saved to: {report_file}")
    print(f"JSON results saved to: {json_file}")


if __name__ == "__main__":
    main()