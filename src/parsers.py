import re
from pathlib import Path
from typing import List, Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent
MOCK_DATA_DIR = BASE_DIR / "mock_data" / "cisco_ios"


def load_mock_file(filename: str) -> str:
    """Safely reads and returns the raw string content of a mock output file."""
    file_path = MOCK_DATA_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Mock file not found at: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    

def parse_ip_interface_brief(raw_text: str) -> List[Dict[str, Any]]:
    """Parses 'show ip interface brief' command output into structured data."""
    parsed_interfaces = []

    pattern = re.compile(
        r"^(?P<interface>\S+)\s+(?P<ip_address>\S+)\s+\w+\s+\w+\s+(?P<status>up|down|administratively down)\s+(?P<protocol>up|down)\s*$",
        re.MULTILINE
    )

    for match in pattern.finditer(raw_text):
        parsed_interfaces.append(match.groupdict())

    return parsed_interfaces


def parse_bgp_summary(raw_text: str) -> List[Dict[str, Any]]:
    """Parses 'show ip bgp summary' neighbor table into structured data."""
    parsed_neighbors = []

    pattern = re.compile(
        r"^(?P<neighbor>[0-9.]+)\s+\d+\s+(?P<asn>\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(?P<up_down>\S+)\s+(?P<state_pfx>\S+)\s*$",
        re.MULTILINE
    )

    for match in pattern.finditer(raw_text):
        data = match.groupdict()
        data["asn"] = int(data["asn"])
        parsed_neighbors.append(data)

    return parsed_neighbors