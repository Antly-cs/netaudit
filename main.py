from src.parsers import load_mock_file, parse_ip_interface_brief, parse_bgp_summary

def main():
    print("--- Testing 'show ip interface brief' Parser ---")
    int_brief_raw = load_mock_file("cr01.london_show_ip_int_brief.txt")
    interfaces = parse_ip_interface_brief(int_brief_raw)
    for interface in interfaces:
        print(interface)

    print("\n--- Testing 'show bgp summary' Parser ---")
    bgp_raw = load_mock_file("cr01.london_show_bgp_summary.txt")
    neighbors = parse_bgp_summary(bgp_raw)
    for neighbor in neighbors:
        print(neighbor)

if __name__ == "__main__":
    main()