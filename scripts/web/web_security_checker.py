#!/usr/bin/env python3
"""
Web Application Security Checker
Performs basic security checks on web applications.
"""

import requests
import argparse
import json
import sys
from datetime import datetime
from typing import Dict, Any, List
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import re
from bs4 import BeautifulSoup

class WebSecurityChecker:
    def __init__(self, target: str, threads: int = 5):
        """
        Initialize the web security checker.
        
        Args:
            target: Target URL
            threads: Number of threads to use
        """
        self.target = target if target.startswith(('http://', 'https://')) else f'https://{target}'
        self.threads = threads
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'SecurityChecker/1.0'})
        self.results: Dict[str, Any] = {
            "target": target,
            "scan_time": datetime.now().isoformat(),
            "security_headers": {},
            "ssl_info": {},
            "findings": [],
            "forms": [],
            "endpoints": [],
            "vulnerabilities": []
        }

    def check_security_headers(self) -> Dict[str, str]:
        """
        Check for security-related HTTP headers.
        
        Returns:
            Dictionary of security headers and their values
        """
        try:
            response = self.session.get(self.target)
            headers = response.headers
            
            security_headers = {
                'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'Not Set'),
                'X-Frame-Options': headers.get('X-Frame-Options', 'Not Set'),
                'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'Not Set'),
                'Content-Security-Policy': headers.get('Content-Security-Policy', 'Not Set'),
                'X-XSS-Protection': headers.get('X-XSS-Protection', 'Not Set'),
                'Referrer-Policy': headers.get('Referrer-Policy', 'Not Set'),
                'Feature-Policy': headers.get('Feature-Policy', 'Not Set'),
                'Access-Control-Allow-Origin': headers.get('Access-Control-Allow-Origin', 'Not Set'),
                'Server': headers.get('Server', 'Not Set')
            }
            
            return security_headers
            
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def check_ssl(self) -> Dict[str, Any]:
        """
        Check SSL/TLS configuration.
        
        Returns:
            Dictionary containing SSL information
        """
        try:
            response = self.session.get(self.target)
            cert = response.raw.connection.sock.getpeercert()
            
            return {
                "version": response.raw.connection.sock.version(),
                "cipher": response.raw.connection.sock.cipher(),
                "certificate": {
                    "subject": dict(x[0] for x in cert['subject']),
                    "issuer": dict(x[0] for x in cert['issuer']),
                    "expires": cert['notAfter']
                }
            }
            
        except Exception as e:
            return {"error": str(e)}

    def discover_endpoints(self) -> List[str]:
        """
        Discover endpoints from HTML content.
        
        Returns:
            List of discovered endpoints
        """
        endpoints = set()
        try:
            response = self.session.get(self.target)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/') or self.target in href:
                    endpoints.add(urljoin(self.target, href))
                    
            # Find all forms
            for form in soup.find_all('form'):
                action = form.get('action', '')
                if action:
                    endpoints.add(urljoin(self.target, action))
                    
            # Find script sources
            for script in soup.find_all('script', src=True):
                src = script['src']
                endpoints.add(urljoin(self.target, src))
                
            return list(endpoints)
            
        except Exception as e:
            return []

    def analyze_form(self, form_url: str) -> Dict[str, Any]:
        """
        Analyze a form for security issues.
        
        Args:
            form_url: URL of the form to analyze
            
        Returns:
            Dictionary containing form analysis results
        """
        try:
            response = self.session.get(form_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = []
            
            for form in soup.find_all('form'):
                form_info = {
                    "action": form.get('action', ''),
                    "method": form.get('method', 'get').upper(),
                    "inputs": [],
                    "csrf_protection": False,
                    "issues": []
                }
                
                # Check inputs
                for input_field in form.find_all('input'):
                    input_type = input_field.get('type', '')
                    input_name = input_field.get('name', '')
                    
                    form_info["inputs"].append({
                        "type": input_type,
                        "name": input_name,
                        "autocomplete": input_field.get('autocomplete', '')
                    })
                    
                    # Check for security issues
                    if input_type == 'password' and 'autocomplete' not in input_field.attrs:
                        form_info["issues"].append("Password field without autocomplete=off")
                        
                # Check for CSRF protection
                csrf_tokens = form.find_all('input', attrs={
                    "type": "hidden",
                    "name": re.compile(r"csrf|token", re.I)
                })
                
                form_info["csrf_protection"] = len(csrf_tokens) > 0
                if not form_info["csrf_protection"] and form_info["method"] == "POST":
                    form_info["issues"].append("No CSRF protection detected")
                    
                forms.append(form_info)
                
            return forms
            
        except Exception as e:
            return [{"error": str(e)}]

    def test_xss(self, url: str) -> List[Dict[str, Any]]:
        """
        Test for basic XSS vulnerabilities.
        
        Args:
            url: URL to test
            
        Returns:
            List of potential XSS vulnerabilities
        """
        xss_payloads = [
            "<script>alert(1)</script>",
            "'-alert(1)-'",
            "\"><script>alert(1)</script>",
            "<img src=x onerror=alert(1)>"
        ]
        
        findings = []
        parsed = urlparse(url)
        
        if not parsed.query:
            return findings
            
        for payload in xss_payloads:
            test_url = url.replace('=', f'={payload}')
            try:
                response = self.session.get(test_url)
                if payload in response.text:
                    findings.append({
                        "type": "xss",
                        "url": test_url,
                        "payload": payload,
                        "severity": "high"
                    })
            except:
                continue
                
        return findings

    def check(self) -> Dict[str, Any]:
        """
        Perform the web security check.
        
        Returns:
            Dictionary containing all check results
        """
        print(f"[*] Starting web security check of {self.target}")
        
        # Check security headers
        print("[*] Checking security headers")
        self.results["security_headers"] = self.check_security_headers()
        
        # Check SSL/TLS
        print("[*] Checking SSL/TLS configuration")
        self.results["ssl_info"] = self.check_ssl()
        
        # Discover endpoints
        print("[*] Discovering endpoints")
        self.results["endpoints"] = self.discover_endpoints()
        
        # Analyze forms
        print("[*] Analyzing forms")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            form_results = list(executor.map(self.analyze_form, self.results["endpoints"]))
            for forms in form_results:
                self.results["forms"].extend(forms)
                
        # Test for vulnerabilities
        print("[*] Testing for vulnerabilities")
        for endpoint in self.results["endpoints"]:
            if '=' in endpoint:  # Only test endpoints with parameters
                xss_findings = self.test_xss(endpoint)
                self.results["vulnerabilities"].extend(xss_findings)
                
        # Assess findings
        self.assess_security_posture()
        
        return self.results

    def assess_security_posture(self) -> None:
        """
        Assess the overall security posture based on findings.
        """
        # Check security headers
        for header, value in self.results["security_headers"].items():
            if value == 'Not Set':
                self.results["findings"].append({
                    "type": "missing_header",
                    "header": header,
                    "severity": "medium",
                    "description": f"Security header {header} is not set"
                })

        # Check SSL/TLS
        ssl_info = self.results["ssl_info"]
        if "error" not in ssl_info:
            version = ssl_info.get("version", "")
            if version and any(v in version for v in ['SSLv2', 'SSLv3', 'TLSv1.0', 'TLSv1.1']):
                self.results["findings"].append({
                    "type": "weak_ssl",
                    "version": version,
                    "severity": "high",
                    "description": f"Weak SSL/TLS version {version} in use"
                })

        # Check forms
        for form in self.results["forms"]:
            if "issues" in form:
                for issue in form["issues"]:
                    self.results["findings"].append({
                        "type": "form_issue",
                        "form": form.get("action", "unknown"),
                        "severity": "medium",
                        "description": issue
                    })

def main():
    parser = argparse.ArgumentParser(description="Web Application Security Checker")
    parser.add_argument("target", help="Target URL")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads (default: 5)")
    parser.add_argument("-o", "--output", help="Output file for results", default="web_security_check.json")
    args = parser.parse_args()

    try:
        checker = WebSecurityChecker(args.target, args.threads)
        results = checker.check()

        # Save results
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"\n[+] Check completed. Results saved to {args.output}")
        
        # Print summary
        print("\nCheck Summary:")
        print(f"Endpoints Discovered: {len(results['endpoints'])}")
        print(f"Forms Analyzed: {len(results['forms'])}")
        print(f"Vulnerabilities Found: {len(results['vulnerabilities'])}")
        print(f"Security Findings: {len(results['findings'])}")
        
        print("\nKey Findings:")
        for finding in results["findings"]:
            print(f"- {finding['severity'].upper()}: {finding['description']}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()