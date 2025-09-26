#!/usr/bin/env python3
"""
Security Assessment Toolkit - Main Launcher
A comprehensive security assessment toolkit for conducting tiered cybersecurity assessments
"""

import sys
import os
import argparse
from datetime import datetime

def main():
    """Main launcher for the Security Assessment Toolkit"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        Security Assessment Toolkit                           ║
║                                                                               ║
║  A comprehensive security assessment toolkit for conducting tiered           ║
║  cybersecurity assessments for individuals, small businesses,                ║
║  and application security reviews.                                           ║
║                                                                               ║
║  Frameworks: ASD Essential Eight, NIST CSF                                   ║
║  Tools: VirtualBox, Vagrant, Wireshark, BurpSuite                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    parser = argparse.ArgumentParser(
        description="Security Assessment Toolkit - Comprehensive cybersecurity assessment platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --tier individual                    # Run individual security assessment
  %(prog)s --tier small-business               # Run small business assessment
  %(prog)s --tier application                  # Run application security assessment
  %(prog)s --framework asd-essential-eight     # Run ASD Essential Eight assessment
  %(prog)s --framework nist-csf                # Run NIST CSF assessment
  %(prog)s --scan network --target 192.168.1.1 # Run network security scan
  %(prog)s --scan system                       # Run system hardening check
  %(prog)s --integration wireshark --pcap file.pcap # Analyze pcap with Wireshark
  %(prog)s --integration burpsuite --target https://example.com # Web app scan
  %(prog)s --setup vagrant                     # Set up Vagrant testing environment
  %(prog)s --help-guides                       # Show available guides and documentation
        """
    )
    
    # Main action groups
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        '--tier',
        choices=['individual', 'small-business', 'application'],
        help='Run tier-specific security assessment'
    )
    
    group.add_argument(
        '--framework',
        choices=['asd-essential-eight', 'nist-csf'],
        help='Run framework-specific assessment'
    )
    
    group.add_argument(
        '--scan',
        choices=['network', 'system'],
        help='Run automated security scans'
    )
    
    group.add_argument(
        '--integration',
        choices=['wireshark', 'burpsuite'],
        help='Use tool integrations'
    )
    
    group.add_argument(
        '--setup',
        choices=['vagrant', 'virtualbox'],
        help='Set up testing environments'
    )
    
    group.add_argument(
        '--help-guides',
        action='store_true',
        help='Show available guides and documentation'
    )
    
    # Additional options
    parser.add_argument('--target', help='Target for scans (IP, URL, etc.)')
    parser.add_argument('--pcap', help='PCAP file for Wireshark analysis')
    parser.add_argument('--output', help='Output directory for reports')
    parser.add_argument('--config', help='Configuration file path')
    
    args = parser.parse_args()
    
    # Set up output directory
    if args.output:
        output_dir = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"results_{timestamp}"
    
    os.makedirs(output_dir, exist_ok=True)
    os.chdir(output_dir)
    
    # Execute based on arguments
    if args.tier:
        run_tier_assessment(args.tier)
    elif args.framework:
        run_framework_assessment(args.framework)
    elif args.scan:
        run_security_scan(args.scan, args.target)
    elif args.integration:
        run_tool_integration(args.integration, args.target, args.pcap)
    elif args.setup:
        setup_environment(args.setup)
    elif args.help_guides:
        show_guides()


def run_tier_assessment(tier: str):
    """Run tier-specific security assessment"""
    print(f"\n🎯 Running {tier} tier security assessment...")
    
    if tier == 'individual':
        os.system(f"python3 {get_script_path()}/tiers/individual/assessment.py")
    elif tier == 'small-business':
        os.system(f"python3 {get_script_path()}/tiers/small-business/assessment.py")
    elif tier == 'application':
        os.system(f"python3 {get_script_path()}/tiers/application/assessment.py")


def run_framework_assessment(framework: str):
    """Run framework-specific assessment"""
    print(f"\n📋 Running {framework} framework assessment...")
    
    if framework == 'asd-essential-eight':
        os.system(f"python3 {get_script_path()}/frameworks/asd-essential-eight/assessment.py")
    elif framework == 'nist-csf':
        os.system(f"python3 {get_script_path()}/frameworks/nist-csf/assessment.py")


def run_security_scan(scan_type: str, target: str):
    """Run automated security scans"""
    print(f"\n🔍 Running {scan_type} security scan...")
    
    if scan_type == 'network':
        if not target:
            print("❌ Network scan requires --target parameter")
            sys.exit(1)
        os.system(f"python3 {get_script_path()}/scripts/automated-checks/network_scan.py {target}")
    elif scan_type == 'system':
        os.system(f"python3 {get_script_path()}/scripts/automated-checks/system_hardening_check.py")


def run_tool_integration(tool: str, target: str, pcap_file: str):
    """Run tool integrations"""
    print(f"\n🔧 Running {tool} integration...")
    
    if tool == 'wireshark':
        if pcap_file:
            os.system(f"python3 {get_script_path()}/scripts/integrations/wireshark/packet_analysis.py {pcap_file}")
        else:
            print("❌ Wireshark integration requires --pcap parameter")
            print("Usage: --integration wireshark --pcap file.pcap")
            sys.exit(1)
    elif tool == 'burpsuite':
        if target:
            os.system(f"python3 {get_script_path()}/scripts/integrations/burpsuite/api_scanner.py {target}")
        else:
            print("❌ BurpSuite integration requires --target parameter")
            print("Usage: --integration burpsuite --target https://example.com")
            sys.exit(1)


def setup_environment(env_type: str):
    """Set up testing environments"""
    print(f"\n⚙️  Setting up {env_type} environment...")
    
    if env_type == 'vagrant':
        vagrant_dir = f"{get_script_path()}/environments/vagrant"
        print(f"Vagrant environment directory: {vagrant_dir}")
        print("\nTo set up the Vagrant environment:")
        print(f"1. cd {vagrant_dir}")
        print("2. vagrant up")
        print("3. vagrant ssh")
        print("\nThis will create a fully configured security testing environment.")
    elif env_type == 'virtualbox':
        print("VirtualBox setup instructions:")
        print("1. Install VirtualBox from https://www.virtualbox.org/")
        print("2. Use the provided Vagrant configuration for automated setup")
        print("3. Or manually create VMs using the guides in the documentation")


def show_guides():
    """Show available guides and documentation"""
    print("\n📚 Available Guides and Documentation:")
    print("="*50)
    
    guides_dir = f"{get_script_path()}/guides"
    
    print("\n🎯 Assessment Guides:")
    print("• Individual Tier Assessment Guide")
    print("• Small Business Security Assessment Guide") 
    print("• Application Security Assessment Guide")
    
    print("\n📋 Framework Guides:")
    print("• ASD Essential Eight Implementation Guide")
    print("• NIST Cybersecurity Framework Guide")
    
    print("\n🔧 Tool Integration Guides:")
    print("• Wireshark Network Analysis Guide")
    print("• BurpSuite Web Application Testing Guide")
    print("• Vagrant Testing Environment Setup")
    
    print("\n📖 Templates and Examples:")
    print("• Assessment Report Templates")
    print("• Security Policy Templates")
    print("• Incident Response Templates")
    
    print(f"\nGuides location: {guides_dir}")
    print("\nFor detailed documentation, see README.md in the toolkit directory.")


def get_script_path() -> str:
    """Get the path to the toolkit scripts"""
    # Get the directory where main.py is located
    return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    main()