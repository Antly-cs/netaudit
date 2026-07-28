from src.parsers import load_mock_file, parse_ip_interface_brief, parse_bgp_summary
from src.validators import Interface, BGPNeighbor
from pydantic import ValidationError

def main():
    print("--- Running Interface Audit ---")
    int_brief_raw = load_mock_file("cr01.london_show_ip_int_brief.txt")
    interfaces_data = parse_ip_interface_brief(int_brief_raw)
    
    for data in interfaces_data:
        try:
            # Unpack the dictionary into the Pydantic model
            validated_int = Interface(**data)
            print(f"PASS: {validated_int.interface} ({validated_int.ip_address})")
        except ValidationError as e:
            print(f"❌ FAIL: {data.get('interface')} - {e.errors()[0]['msg']}")

    print("\n--- Running BGP Security Audit ---")
    bgp_raw = load_mock_file("cr01.london_show_bgp_summary.txt")
    bgp_data = parse_bgp_summary(bgp_raw)
    
    for data in bgp_data:
        try:
            validated_bgp = BGPNeighbor(**data)
            print(f"PASS: BGP Peer {validated_bgp.neighbor} is established.")
        except ValidationError as e:
            # Extracting the custom error message we wrote in validators.py
            print(f"AUDIT FLAG: Peer {data.get('neighbor')} - {e.errors()[0]['msg']}")

if __name__ == "__main__":
    main()