import argparse
from src.parsers import load_mock_file, parse_ip_interface_brief, parse_bgp_summary
from src.validators import Interface, BGPNeighbor
from pydantic import ValidationError

def audit_interfaces():
    """Runs the validation rules against the network interfaces."""
    print("\n--- Running Interface Audit ---")
    int_brief_raw = load_mock_file("cr01.london_show_ip_int_brief.txt")
    interfaces_data = parse_ip_interface_brief(int_brief_raw)
    
    for data in interfaces_data:
        try:
            validated_int = Interface(**data)
            print(f"PASS: {validated_int.interface} ({validated_int.ip_address})")
        except ValidationError as e:
            print(f"FAIL: {data.get('interface')} - {e.errors()[0]['msg']}")


def audit_bgp():
    """Runs the validation rules against the BGP routing table."""
    print("\n--- Running BGP Security Audit ---")
    bgp_raw = load_mock_file("cr01.london_show_bgp_summary.txt")
    bgp_data = parse_bgp_summary(bgp_raw)
    
    for data in bgp_data:
        try:
            validated_bgp = BGPNeighbor(**data)
            print(f"PASS: BGP Peer {validated_bgp.neighbor} is established.")
        except ValidationError as e:
            print(f"AUDIT FLAG: Peer {data.get('neighbor')} - {e.errors()[0]['msg']}")


def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="NetAudit: A Python-based network security auditing tool."
    )
    
    # Add a required argument for the user to specify what to audit
    parser.add_argument(
        "--audit", 
        type=str,
        choices=["interfaces", "bgp", "all"],
        required=True,
        help="Specify which network component to audit (interfaces, bgp, or all)."
    )
    
    # Parse the commands typed into the terminal
    args = parser.parse_args()
    
    # Execute the requested functions based on user input
    if args.audit in ["interfaces", "all"]:
        audit_interfaces()
        
    if args.audit in ["bgp", "all"]:
        audit_bgp()


if __name__ == "__main__":
    main()