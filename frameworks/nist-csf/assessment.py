#!/usr/bin/env python3
"""
NIST Cybersecurity Framework (CSF) Assessment
Implements the National Institute of Standards and Technology Cybersecurity Framework
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any


class NISTCSFAssessment:
    """NIST Cybersecurity Framework assessment implementation"""
    
    def __init__(self):
        self.functions = {
            "identify": {
                "name": "Identify (ID)",
                "description": "Develop organizational understanding to manage cybersecurity risk",
                "categories": {
                    "asset_management": {
                        "name": "Asset Management (ID.AM)",
                        "questions": [
                            "Are physical devices and systems inventoried?",
                            "Are software platforms and applications inventoried?",
                            "Are organizational communication and data flows mapped?",
                            "Are external information systems catalogued?"
                        ]
                    },
                    "business_environment": {
                        "name": "Business Environment (ID.BE)",
                        "questions": [
                            "Is the organization's role in the supply chain identified?",
                            "Are the organization's place in critical infrastructure identified?",
                            "Are priorities for organizational mission established?",
                            "Are dependencies and critical functions identified?"
                        ]
                    },
                    "governance": {
                        "name": "Governance (ID.GV)",
                        "questions": [
                            "Is organizational cybersecurity policy established?",
                            "Are cybersecurity roles and responsibilities coordinated?",
                            "Are legal and regulatory requirements understood?",
                            "Is governance and risk management integrated?"
                        ]
                    },
                    "risk_assessment": {
                        "name": "Risk Assessment (ID.RA)",
                        "questions": [
                            "Are asset vulnerabilities identified and documented?",
                            "Are cyber threat intelligence sources identified?",
                            "Are threats to organizational assets identified?",
                            "Are potential business impacts identified?"
                        ]
                    },
                    "risk_management_strategy": {
                        "name": "Risk Management Strategy (ID.RM)",
                        "questions": [
                            "Is risk management strategy established?",
                            "Are organizational risk tolerances determined?",
                            "Is risk determination repeatable and consistent?",
                            "Are risk response strategies determined?"
                        ]
                    }
                }
            },
            "protect": {
                "name": "Protect (PR)",
                "description": "Develop and implement appropriate safeguards",
                "categories": {
                    "access_control": {
                        "name": "Access Control (PR.AC)",
                        "questions": [
                            "Are identities and credentials managed for users and devices?",
                            "Is physical access to assets managed?",
                            "Is remote access managed?",
                            "Are access permissions managed consistent with least privilege?"
                        ]
                    },
                    "awareness_training": {
                        "name": "Awareness and Training (PR.AT)",
                        "questions": [
                            "Are all users informed and trained?",
                            "Are privileged users trained for their roles?",
                            "Are third-party stakeholders trained?",
                            "Are senior executives trained?"
                        ]
                    },
                    "data_security": {
                        "name": "Data Security (PR.DS)",
                        "questions": [
                            "Is data-at-rest protected?",
                            "Is data-in-transit protected?",
                            "Are assets formally managed throughout removal?",
                            "Is adequate capacity maintained?"
                        ]
                    },
                    "information_protection": {
                        "name": "Information Protection Processes (PR.IP)",
                        "questions": [
                            "Is a baseline configuration established?",
                            "Is a system development life cycle managed?",
                            "Are configuration change control processes in place?",
                            "Are backups conducted, maintained, and tested?"
                        ]
                    },
                    "maintenance": {
                        "name": "Maintenance (PR.MA)",
                        "questions": [
                            "Is maintenance performed and logged?",
                            "Is remote maintenance approved and logged?",
                            "Are maintenance tools approved and monitored?",
                            "Are spare parts and media handled securely?"
                        ]
                    },
                    "protective_technology": {
                        "name": "Protective Technology (PR.PT)",
                        "questions": [
                            "Are audit/log records determined and generated?",
                            "Is removable media protected?",
                            "Are systems protected at network boundaries?",
                            "Are communications and control networks protected?"
                        ]
                    }
                }
            },
            "detect": {
                "name": "Detect (DE)",
                "description": "Develop and implement activities to identify occurrence of cybersecurity events",
                "categories": {
                    "anomalies_events": {
                        "name": "Anomalies and Events (DE.AE)",
                        "questions": [
                            "Is a baseline of network operations established?",
                            "Are detected events analyzed?",
                            "Is event data aggregated and correlated?",
                            "Is the impact of events determined?"
                        ]
                    },
                    "security_monitoring": {
                        "name": "Security Continuous Monitoring (DE.CM)",
                        "questions": [
                            "Is the network monitored for unauthorized activity?",
                            "Is the physical environment monitored?",
                            "Are personnel activity and external service provider monitored?",
                            "Are malicious code detections monitored?"
                        ]
                    },
                    "detection_processes": {
                        "name": "Detection Processes (DE.DP)",
                        "questions": [
                            "Are roles and responsibilities defined?",
                            "Are detection activities comply with requirements?",
                            "Are detection processes tested?",
                            "Is event detection information communicated?"
                        ]
                    }
                }
            },
            "respond": {
                "name": "Respond (RS)",
                "description": "Develop and implement activities to take action regarding detected cybersecurity incident",
                "categories": {
                    "response_planning": {
                        "name": "Response Planning (RS.RP)",
                        "questions": [
                            "Is response plan executed during or after incident?",
                            "Are response procedures updated?",
                            "Is response plan tested?",
                            "Are personnel trained on response procedures?"
                        ]
                    },
                    "communications": {
                        "name": "Communications (RS.CO)",
                        "questions": [
                            "Are personnel aware of their roles?",
                            "Are events reported consistent with criteria?",
                            "Is information shared with stakeholders?",
                            "Is coordination with law enforcement performed?"
                        ]
                    },
                    "analysis": {
                        "name": "Analysis (RS.AN)",
                        "questions": [
                            "Are notifications investigated?",
                            "Is the impact understood?",
                            "Is forensics performed?",
                            "Are incidents categorized?"
                        ]
                    },
                    "mitigation": {
                        "name": "Mitigation (RS.MI)",
                        "questions": [
                            "Are incidents contained?",
                            "Are incidents mitigated?",
                            "Are newly identified vulnerabilities mitigated?"
                        ]
                    },
                    "improvements": {
                        "name": "Improvements (RS.IM)",
                        "questions": [
                            "Are response plans updated?",
                            "Are response strategies updated?",
                            "Are lessons learned incorporated?"
                        ]
                    }
                }
            },
            "recover": {
                "name": "Recover (RC)",
                "description": "Develop and implement activities to maintain resilience and restore services",
                "categories": {
                    "recovery_planning": {
                        "name": "Recovery Planning (RC.RP)",
                        "questions": [
                            "Is recovery plan executed during or after incident?",
                            "Is recovery plan updated?",
                            "Is recovery plan tested?",
                            "Are personnel trained on recovery procedures?"
                        ]
                    },
                    "improvements": {
                        "name": "Improvements (RC.IM)",
                        "questions": [
                            "Are recovery plans updated?",
                            "Are recovery strategies updated?",
                            "Are lessons learned incorporated?"
                        ]
                    },
                    "communications": {
                        "name": "Communications (RC.CO)",
                        "questions": [
                            "Are public relations managed?",
                            "Are reputation repaired?",
                            "Are recovery activities communicated internally?",
                            "Are recovery activities communicated externally?"
                        ]
                    }
                }
            }
        }
        self.results = {}
    
    def conduct_assessment(self, organization_name: str = "Unknown Organization") -> Dict[str, Any]:
        """Conduct the NIST CSF assessment"""
        print(f"NIST Cybersecurity Framework Assessment for: {organization_name}")
        print("=" * 60)
        
        self.results = {
            "organization": organization_name,
            "assessment_date": datetime.now().isoformat(),
            "framework": "NIST Cybersecurity Framework",
            "functions": {}
        }
        
        for function_key, function in self.functions.items():
            print(f"\n{function['name']}")
            print("-" * len(function['name']))
            print(f"Description: {function['description']}")
            
            function_results = {
                "name": function['name'],
                "description": function['description'],
                "categories": {},
                "overall_score": 0.0
            }
            
            category_scores = []
            
            for category_key, category in function['categories'].items():
                print(f"\n  {category['name']}")
                print("  " + "-" * len(category['name']))
                
                category_results = {
                    "name": category['name'],
                    "responses": {},
                    "score": 0.0,
                    "tier": "Partial"
                }
                
                question_scores = []
                
                for i, question in enumerate(category['questions']):
                    print(f"    Q{i+1}: {question}")
                    
                    # Simulate response (in real implementation, this would be interactive)
                    response = self._simulate_response()
                    score = self._calculate_question_score(response)
                    
                    category_results['responses'][f"q{i+1}"] = {
                        "question": question,
                        "answer": response,
                        "score": score
                    }
                    question_scores.append(score)
                
                # Calculate category score and tier
                category_score = sum(question_scores) / len(question_scores)
                category_results['score'] = category_score
                category_results['tier'] = self._determine_tier(category_score)
                
                function_results['categories'][category_key] = category_results
                category_scores.append(category_score)
            
            # Calculate function overall score
            function_results['overall_score'] = sum(category_scores) / len(category_scores)
            self.results['functions'][function_key] = function_results
        
        return self.results
    
    def _simulate_response(self) -> str:
        """Simulate assessment responses for demonstration"""
        import random
        responses = [
            "Fully implemented and regularly reviewed",
            "Mostly implemented with some gaps",
            "Partially implemented",
            "Minimally implemented",
            "Not implemented"
        ]
        return random.choice(responses)
    
    def _calculate_question_score(self, response: str) -> float:
        """Calculate numeric score from response"""
        response_lower = response.lower()
        if "fully implemented" in response_lower:
            return 4.0
        elif "mostly implemented" in response_lower:
            return 3.0
        elif "partially implemented" in response_lower:
            return 2.0
        elif "minimally implemented" in response_lower:
            return 1.0
        else:
            return 0.0
    
    def _determine_tier(self, score: float) -> str:
        """Determine NIST CSF implementation tier based on score"""
        if score >= 3.5:
            return "Adaptive"
        elif score >= 2.5:
            return "Repeatable"
        elif score >= 1.5:
            return "Risk Informed"
        else:
            return "Partial"
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate assessment report"""
        if not self.results:
            raise ValueError("No assessment results available. Run conduct_assessment() first.")
        
        report = f"""
NIST Cybersecurity Framework Assessment Report
============================================

Organization: {self.results['organization']}
Assessment Date: {self.results['assessment_date']}
Framework: {self.results['framework']}

Executive Summary:
"""
        
        # Calculate overall maturity
        function_scores = [f['overall_score'] for f in self.results['functions'].values()]
        overall_score = sum(function_scores) / len(function_scores)
        overall_tier = self._determine_tier(overall_score)
        
        report += f"Overall Implementation Tier: {overall_tier} ({overall_score:.2f}/4.0)\n\n"
        
        report += "Function Assessment Results:\n"
        report += "-" * 30 + "\n"
        
        for function_key, function in self.results['functions'].items():
            report += f"\n{function['name']}: {function['overall_score']:.2f}/4.0\n"
            
            for category_key, category in function['categories'].items():
                report += f"  {category['name']}: {category['tier']} ({category['score']:.2f}/4.0)\n"
        
        # Add recommendations
        report += "\nRecommendations:\n"
        report += "-" * 15 + "\n"
        
        for function_key, function in self.results['functions'].items():
            if function['overall_score'] < 2.0:
                report += f"- Priority: Improve {function['name']} capabilities\n"
        
        if overall_score < 2.5:
            report += "- Focus on establishing consistent risk management processes\n"
            report += "- Implement formal incident response procedures\n"
        
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
    assessment = NISTCSFAssessment()
    
    org_name = input("Enter organization name (or press Enter for default): ").strip()
    if not org_name:
        org_name = "Unknown Organization"
    
    print("\nStarting NIST Cybersecurity Framework Assessment...")
    results = assessment.conduct_assessment(org_name)
    
    # Generate and save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"nist_csf_report_{timestamp}.txt"
    json_file = f"nist_csf_results_{timestamp}.json"
    
    report = assessment.generate_report(report_file)
    assessment.export_json(json_file)
    
    print("\n" + "="*60)
    print("ASSESSMENT COMPLETE")
    print(f"Report saved to: {report_file}")
    print(f"JSON results saved to: {json_file}")


if __name__ == "__main__":
    main()