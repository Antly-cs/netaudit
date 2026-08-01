# Cisco Config Auditor | Network Security Compliance Engine

An automated, CLI-based security auditing tool built in Python. Cisco Config Auditor validates Cisco IOS network configurations against security baselines, identifies misconfigurations (like unassigned active interfaces), and detects BGP peering anomalies. 

This tool is designed with enterprise SOC integration in mind, outputting structured JSON reports ready for SIEM ingestion (e.g., Wazuh, Splunk).

![Terminal Output](assets/terminal-output.jpeg)

## Key Features

* **CLI Automation:** Lightweight command-line interface built with `argparse` for seamless integration into cron jobs and CI/CD pipelines.
* **Custom Parsing Engine:** Utilizes Python Regular Expressions (`re`) to extract structured data streams from raw Cisco terminal output (`show ip interface brief`, `show ip bgp summary`).
* **Strict Data Validation:** Leverages **Pydantic** object-oriented models to enforce strict type-checking and validate security states (e.g., flagging 'Active' BGP connection state failures).
* **SIEM-Ready Logging:** Automatically generates timestamped JSON audit reports to bridge the gap between network state and automated SOC incident response workflows.

## Technology Stack

* **Language:** Python 3.x
* **Core Libraries:** `pydantic`, `argparse`, `re`, `json`, `ipaddress`
* **Target Environment:** Cisco IOS / Simulated Lab Environments (GNS3 / EVE-NG)

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Antly-cs/cisco-config-auditor.git](https://github.com/Antly-cs/cisco-config-auditor.git)
   cd cisco-config-auditor
   ```

2. **Install dependencies:**
   ```bash
   pip install pydantic
   ```

3. **Run the CLI tool:**
   ```bash
   # Audit only interfaces
   python main.py --audit interfaces

   # Audit only BGP peers
   python main.py --audit bgp

   # Run a full security sweep
   python main.py --audit all
   ```

## Example JSON Output

When a full audit is executed, Cisco Config Auditor generates a timestamped report in the `/reports` directory. 

```json
[
    {
        "component": "interface",
        "target": "GigabitEthernet1",
        "status": "PASS",
        "details": "Configuration valid"
    },
    {
        "component": "bgp",
        "target": "10.0.0.2",
        "status": "PASS",
        "details": "Peer established"
    },
    {
        "component": "bgp",
        "target": "192.168.1.2",
        "status": "FAIL",
        "details": "Value error, Insecure/Down BGP State detected: 'Active'."
    }
]
```