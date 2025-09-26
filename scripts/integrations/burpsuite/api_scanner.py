#!/usr/bin/env python3
"""
Burp Suite Integration Script
API and web application security scanning integration
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, List, Any
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET


class BurpSuiteIntegration:
    """Burp Suite Professional API integration for automated scanning"""
    
    def __init__(self, burp_url: str = "http://127.0.0.1:1337", api_key: str = None):
        self.burp_url = burp_url
        self.api_key = api_key
        self.session = requests.Session()
        
        # Set API key if provided
        if api_key:
            self.session.headers.update({"X-API-Key": api_key})
        
        self.results = {
            "scan_date": datetime.now().isoformat(),
            "scanner": "Burp Suite Integration",
            "scans": {},
            "vulnerabilities": []
        }
    
    def check_burp_connection(self) -> bool:
        """Check if Burp Suite is running and API is accessible"""
        try:
            response = self.session.get(f"{self.burp_url}/burp/versions")
            if response.status_code == 200:
                version_info = response.json()
                print(f"✓ Connected to Burp Suite {version_info.get('burp', 'Unknown version')}")
                return True
            else:
                print(f"✗ Burp Suite API not accessible: HTTP {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("✗ Cannot connect to Burp Suite. Ensure Burp is running with API enabled.")
            return False
        except Exception as e:
            print(f"✗ Error connecting to Burp Suite: {e}")
            return False
    
    def start_scan(self, target_url: str, scan_config: str = "Crawl and Audit - Fast") -> str:
        """Start a new scan task"""
        print(f"Starting scan of {target_url}...")
        
        scan_data = {
            "urls": [target_url],
            "scan_configurations": [
                {
                    "name": scan_config,
                    "type": "NamedConfiguration"
                }
            ]
        }
        
        try:
            # Start the scan
            response = self.session.post(
                f"{self.burp_url}/burp/scanner/scans/active",
                json=scan_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                scan_info = response.json()
                scan_id = scan_info.get("task_id")
                print(f"✓ Scan started with ID: {scan_id}")
                
                self.results["scans"][scan_id] = {
                    "target_url": target_url,
                    "scan_config": scan_config,
                    "start_time": datetime.now().isoformat(),
                    "status": "running"
                }
                
                return scan_id
            else:
                print(f"✗ Failed to start scan: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"✗ Error starting scan: {e}")
            return None
    
    def get_scan_status(self, scan_id: str) -> Dict[str, Any]:
        """Get the status of a running scan"""
        try:
            response = self.session.get(f"{self.burp_url}/burp/scanner/scans/{scan_id}")
            
            if response.status_code == 200:
                scan_status = response.json()
                return scan_status
            else:
                print(f"✗ Error getting scan status: HTTP {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"✗ Error getting scan status: {e}")
            return {}
    
    def wait_for_scan_completion(self, scan_id: str, timeout: int = 3600) -> bool:
        """Wait for scan to complete with timeout"""
        print(f"Waiting for scan {scan_id} to complete...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_scan_status(scan_id)
            
            if status:
                scan_status = status.get("scan_status", "unknown")
                print(f"Scan status: {scan_status}")
                
                if scan_status in ["succeeded", "failed", "cancelled"]:
                    self.results["scans"][scan_id]["status"] = scan_status
                    self.results["scans"][scan_id]["end_time"] = datetime.now().isoformat()
                    return scan_status == "succeeded"
            
            time.sleep(30)  # Check every 30 seconds
        
        print(f"✗ Scan timed out after {timeout} seconds")
        return False
    
    def get_scan_issues(self, scan_id: str) -> List[Dict[str, Any]]:
        """Get issues/vulnerabilities found in the scan"""
        try:
            response = self.session.get(f"{self.burp_url}/burp/scanner/scans/{scan_id}/issues")
            
            if response.status_code == 200:
                issues = response.json()
                print(f"✓ Retrieved {len(issues)} issues from scan")
                return issues
            else:
                print(f"✗ Error getting scan issues: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"✗ Error getting scan issues: {e}")
            return []
    
    def generate_burp_report(self, scan_id: str, format: str = "HTML") -> str:
        """Generate a report for the scan"""
        report_data = {
            "scan_id": scan_id,
            "report_type": format,
            "include_false_positives": False
        }
        
        try:
            response = self.session.post(
                f"{self.burp_url}/burp/scanner/scans/{scan_id}/report",
                json=report_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_file = f"burp_report_{scan_id}_{timestamp}.{format.lower()}"
                
                with open(report_file, 'wb') as f:
                    f.write(response.content)
                
                print(f"✓ Report saved: {report_file}")
                return report_file
            else:
                print(f"✗ Error generating report: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Error generating report: {e}")
            return None
    
    def passive_scan_proxy_history(self) -> List[Dict[str, Any]]:
        """Run passive scan on proxy history"""
        print("Running passive scan on proxy history...")
        
        try:
            # Get proxy history
            response = self.session.get(f"{self.burp_url}/burp/proxy/history")
            
            if response.status_code == 200:
                history = response.json()
                print(f"✓ Found {len(history)} items in proxy history")
                
                # Start passive scan
                response = self.session.post(f"{self.burp_url}/burp/scanner/scans/passive")
                
                if response.status_code == 201:
                    print("✓ Passive scan started on proxy history")
                    return history
                else:
                    print(f"✗ Failed to start passive scan: HTTP {response.status_code}")
                    return []
            else:
                print(f"✗ Error getting proxy history: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"✗ Error with passive scan: {e}")
            return []
    
    def spider_target(self, target_url: str) -> bool:
        """Spider/crawl the target application"""
        print(f"Spidering {target_url}...")
        
        spider_data = {
            "base_url": target_url,
            "max_depth": 10,
            "max_children": 100
        }
        
        try:
            response = self.session.post(
                f"{self.burp_url}/burp/spider",
                json=spider_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                print("✓ Spider started successfully")
                return True
            else:
                print(f"✗ Failed to start spider: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Error starting spider: {e}")
            return False
    
    def analyze_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze and categorize security issues"""
        analysis = {
            "total_issues": len(issues),
            "by_severity": {"High": 0, "Medium": 0, "Low": 0, "Information": 0},
            "by_confidence": {"Certain": 0, "Firm": 0, "Tentative": 0},
            "by_type": {},
            "critical_issues": [],
            "owasp_top10": {}
        }
        
        # OWASP Top 10 mapping
        owasp_mapping = {
            "SQL injection": "A03 - Injection",
            "Cross-site scripting": "A03 - Injection", 
            "Cross-site request forgery": "A01 - Broken Access Control",
            "Command injection": "A03 - Injection",
            "Path traversal": "A01 - Broken Access Control",
            "Insecure direct object references": "A01 - Broken Access Control",
            "Missing authentication": "A07 - Identification and Authentication Failures",
            "Weak authentication": "A07 - Identification and Authentication Failures",
            "Information disclosure": "A09 - Security Logging and Monitoring Failures",
            "Insecure cryptographic storage": "A02 - Cryptographic Failures",
            "Insecure communications": "A02 - Cryptographic Failures"
        }
        
        for issue in issues:
            # Count by severity
            severity = issue.get("severity", "Information")
            analysis["by_severity"][severity] = analysis["by_severity"].get(severity, 0) + 1
            
            # Count by confidence
            confidence = issue.get("confidence", "Tentative")
            analysis["by_confidence"][confidence] = analysis["by_confidence"].get(confidence, 0) + 1
            
            # Count by type
            issue_type = issue.get("type_index", "Unknown")
            analysis["by_type"][issue_type] = analysis["by_type"].get(issue_type, 0) + 1
            
            # Identify critical issues
            if severity == "High" and confidence in ["Certain", "Firm"]:
                analysis["critical_issues"].append({
                    "type": issue.get("issue_name", "Unknown"),
                    "url": issue.get("url", ""),
                    "description": issue.get("issue_detail", "")[:200] + "..."
                })
            
            # Map to OWASP Top 10
            issue_name = issue.get("issue_name", "").lower()
            for vuln_type, owasp_cat in owasp_mapping.items():
                if vuln_type in issue_name:
                    analysis["owasp_top10"][owasp_cat] = analysis["owasp_top10"].get(owasp_cat, 0) + 1
                    break
        
        return analysis
    
    def export_to_sarif(self, issues: List[Dict[str, Any]], output_file: str):
        """Export results in SARIF format for integration with other tools"""
        sarif_report = {
            "version": "2.1.0",
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "runs": [{
                "tool": {
                    "driver": {
                        "name": "Burp Suite Scanner",
                        "version": "2023.x",
                        "informationUri": "https://portswigger.net/burp"
                    }
                },
                "results": []
            }]
        }
        
        for issue in issues:
            result = {
                "ruleId": issue.get("type_index", "unknown"),
                "message": {
                    "text": issue.get("issue_name", "Unknown vulnerability")
                },
                "level": self._severity_to_sarif_level(issue.get("severity", "Information")),
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": issue.get("url", "")
                        }
                    }
                }],
                "properties": {
                    "confidence": issue.get("confidence", ""),
                    "description": issue.get("issue_detail", "")
                }
            }
            sarif_report["runs"][0]["results"].append(result)
        
        with open(output_file, 'w') as f:
            json.dump(sarif_report, f, indent=2)
        
        print(f"✓ SARIF report exported: {output_file}")
    
    def _severity_to_sarif_level(self, severity: str) -> str:
        """Convert Burp severity to SARIF level"""
        mapping = {
            "High": "error",
            "Medium": "warning", 
            "Low": "note",
            "Information": "note"
        }
        return mapping.get(severity, "note")
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate comprehensive security assessment report"""
        report = f"""
Burp Suite Security Assessment Report
===================================

Scan Date: {self.results['scan_date']}
Scanner: {self.results['scanner']}

Scan Summary:
"""
        
        total_vulns = len(self.results["vulnerabilities"])
        report += f"Total Vulnerabilities Found: {total_vulns}\n\n"
        
        for scan_id, scan_info in self.results["scans"].items():
            report += f"Scan ID: {scan_id}\n"
            report += f"Target: {scan_info['target_url']}\n"
            report += f"Status: {scan_info['status']}\n"
            report += f"Start Time: {scan_info['start_time']}\n"
            if 'end_time' in scan_info:
                report += f"End Time: {scan_info['end_time']}\n"
            report += "\n"
        
        if self.results["vulnerabilities"]:
            # Analyze vulnerabilities
            analysis = self.analyze_issues(self.results["vulnerabilities"])
            
            report += "Vulnerability Analysis:\n"
            report += "-" * 22 + "\n"
            
            # Severity breakdown
            report += "By Severity:\n"
            for severity, count in analysis["by_severity"].items():
                if count > 0:
                    report += f"  {severity}: {count}\n"
            
            # Critical issues
            if analysis["critical_issues"]:
                report += "\nCritical Issues:\n"
                for i, issue in enumerate(analysis["critical_issues"][:10], 1):
                    report += f"{i}. {issue['type']} at {issue['url']}\n"
                    report += f"   {issue['description']}\n\n"
            
            # OWASP Top 10 mapping
            if analysis["owasp_top10"]:
                report += "OWASP Top 10 Mapping:\n"
                for owasp_cat, count in analysis["owasp_top10"].items():
                    report += f"  {owasp_cat}: {count} issues\n"
        
        report += "\nRecommendations:\n"
        report += "-" * 15 + "\n"
        report += "1. Address all High severity vulnerabilities immediately\n"
        report += "2. Implement proper input validation and sanitization\n"
        report += "3. Use parameterized queries to prevent SQL injection\n"
        report += "4. Implement proper authentication and session management\n"
        report += "5. Regular security testing and code review\n"
        report += "6. Security awareness training for developers\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        
        return report
    
    def export_json(self, output_file: str):
        """Export results as JSON"""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"Results exported to: {output_file}")


class StandaloneBurpScanner:
    """Standalone scanner for when Burp Suite Pro API is not available"""
    
    def __init__(self):
        self.results = {
            "scan_date": datetime.now().isoformat(),
            "scanner": "Standalone Web Security Scanner",
            "findings": []
        }
    
    def basic_web_scan(self, target_url: str) -> List[Dict[str, Any]]:
        """Perform basic web security checks"""
        print(f"Performing basic web security scan of {target_url}...")
        
        findings = []
        
        # Check security headers
        findings.extend(self._check_security_headers(target_url))
        
        # Check for common vulnerabilities
        findings.extend(self._check_common_vulns(target_url))
        
        # Check SSL/TLS configuration
        findings.extend(self._check_ssl_config(target_url))
        
        self.results["findings"] = findings
        return findings
    
    def _check_security_headers(self, url: str) -> List[Dict[str, Any]]:
        """Check for missing security headers"""
        findings = []
        
        try:
            response = requests.get(url, timeout=10, verify=False)
            
            required_headers = {
                "Strict-Transport-Security": "Missing HSTS header",
                "Content-Security-Policy": "Missing CSP header",
                "X-Content-Type-Options": "Missing X-Content-Type-Options header",
                "X-Frame-Options": "Missing X-Frame-Options header",
                "X-XSS-Protection": "Missing X-XSS-Protection header",
                "Referrer-Policy": "Missing Referrer-Policy header"
            }
            
            for header, message in required_headers.items():
                if header not in response.headers:
                    findings.append({
                        "type": "Missing Security Header",
                        "severity": "Medium",
                        "description": message,
                        "url": url,
                        "header": header
                    })
            
            # Check for information disclosure
            info_headers = ["Server", "X-Powered-By", "X-AspNet-Version"]
            for header in info_headers:
                if header in response.headers:
                    findings.append({
                        "type": "Information Disclosure",
                        "severity": "Low",
                        "description": f"Server information disclosed via {header} header",
                        "url": url,
                        "header": header,
                        "value": response.headers[header]
                    })
        
        except Exception as e:
            findings.append({
                "type": "Connection Error",
                "severity": "Information",
                "description": f"Could not connect to {url}: {e}",
                "url": url
            })
        
        return findings
    
    def _check_common_vulns(self, url: str) -> List[Dict[str, Any]]:
        """Check for common web vulnerabilities"""
        findings = []
        
        # Basic XSS test
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>"
        ]
        
        for payload in xss_payloads:
            try:
                test_url = f"{url}?test={payload}"
                response = requests.get(test_url, timeout=10, verify=False)
                
                if payload in response.text:
                    findings.append({
                        "type": "Potential XSS",
                        "severity": "High",
                        "description": "Potential XSS vulnerability detected",
                        "url": test_url,
                        "payload": payload
                    })
                    break  # Don't test all payloads if one works
            except:
                continue
        
        return findings
    
    def _check_ssl_config(self, url: str) -> List[Dict[str, Any]]:
        """Check SSL/TLS configuration"""
        findings = []
        
        if url.startswith('https://'):
            try:
                response = requests.get(url, timeout=10, verify=True)
                # If we get here, SSL cert is valid
            except requests.exceptions.SSLError as e:
                findings.append({
                    "type": "SSL/TLS Issue",
                    "severity": "High",
                    "description": f"SSL/TLS configuration issue: {e}",
                    "url": url
                })
            except:
                pass
        
        return findings


def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python api_scanner.py <target_url> [burp_api_url] [api_key]")
        print("Example: python api_scanner.py https://example.com")
        print("Example: python api_scanner.py https://example.com http://127.0.0.1:1337 your-api-key")
        sys.exit(1)
    
    target_url = sys.argv[1]
    burp_url = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:1337"
    api_key = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Try Burp Suite Professional API first
    burp = BurpSuiteIntegration(burp_url, api_key)
    
    if burp.check_burp_connection():
        print("Using Burp Suite Professional API")
        
        # Start comprehensive scan
        scan_id = burp.start_scan(target_url)
        
        if scan_id:
            # Wait for completion
            if burp.wait_for_scan_completion(scan_id, timeout=1800):  # 30 min timeout
                # Get results
                issues = burp.get_scan_issues(scan_id)
                burp.results["vulnerabilities"] = issues
                
                # Generate Burp report
                burp.generate_burp_report(scan_id, "HTML")
                
                # Export SARIF
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                burp.export_to_sarif(issues, f"burp_scan_results_{timestamp}.sarif")
    else:
        print("Burp Suite Professional not available. Using standalone scanner.")
        
        # Use standalone scanner
        standalone = StandaloneBurpScanner()
        findings = standalone.basic_web_scan(target_url)
        
        # Use standalone results
        burp.results = standalone.results
    
    # Generate and save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"web_security_scan_{timestamp}.txt"
    json_file = f"web_security_results_{timestamp}.json"
    
    report = burp.generate_report(report_file)
    burp.export_json(json_file)
    
    print("\n" + "="*50)
    print("WEB SECURITY SCAN COMPLETE")
    print(f"Report saved to: {report_file}")
    print(f"JSON results saved to: {json_file}")


if __name__ == "__main__":
    main()