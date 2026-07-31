import argparse
import json
import os
from datetime import datetime
from src.parsers import load_mock_file, parse_ip_interface_brief, parse_bgp_summary
from src.validators import Interface, BGPNeighbor
from pydantic import ValidationError

def audit_interfaces():
    print("\n--- Running Interface Audit ---")
    int_brief_raw = load_mock_file("cr01.london_show_ip_int_brief.txt")
    interfaces_data = parse_ip_interface_brief(int_brief_raw)
    
    results = []
    for data in interfaces_data:
        try:
            validated_int = Interface(**data)
            print(f"PASS: {validated_int.interface} ({validated_int.ip_address})")
            results.append({"component": "interface", "target": validated_int.interface, "status": "PASS", "details": "Configuration valid"})
        except ValidationError as e:
            error_msg = e.errors()[0]['msg']
            print(f"FAIL: {data.get('interface')} - {error_msg}")
            results.append({"component": "interface", "target": data.get("interface"), "status": "FAIL", "details": error_msg})
            
    return results


def audit_bgp():
    print("\n--- Running BGP Security Audit ---")
    bgp_raw = load_mock_file("cr01.london_show_bgp_summary.txt")
    bgp_data = parse_bgp_summary(bgp_raw)
    
    results = []
    for data in bgp_data:
        try:
            validated_bgp = BGPNeighbor(**data)
            print(f"PASS: BGP Peer {validated_bgp.neighbor} is established.")
            results.append({"component": "bgp", "target": validated_bgp.neighbor, "status": "PASS", "details": "Peer established"})
        except ValidationError as e:
            error_msg = e.errors()[0]['msg']
            print(f"AUDIT FLAG: Peer {data.get('neighbor')} - {error_msg}")
            results.append({"component": "bgp", "target": data.get("neighbor"), "status": "FAIL", "details": error_msg})
            
    return results


def generate_json_report(audit_data):
    # Create a 'reports' directory if it doesn't exist
    if not os.path.exists("reports"):
        os.makedirs("reports")
        
    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/audit_report_{timestamp}.json"
    
    # Write the data to a JSON file
    with open(filename, "w") as file:
        json.dump(audit_data, file, indent=4)
        
    print(f"\nJSON Audit Report successfully generated: {filename}")


def main():
    parser = argparse.ArgumentParser(description="NetAudit: Network security auditing tool.")
    parser.add_argument("--audit", type=str, choices=["interfaces", "bgp", "all"], required=True, help="Specify what to audit.")
    args = parser.parse_args()
    
    final_report = []
    
    if args.audit in ["interfaces", "all"]:
        final_report.extend(audit_interfaces())
        
    if args.audit in ["bgp", "all"]:
        final_report.extend(audit_bgp())
        
    # Generate the JSON report
    if final_report:
        generate_json_report(final_report)


if __name__ == "__main__":
    main()