from pydantic import BaseModel, field_validator
import ipaddress

class Interface(BaseModel):
    interface: str
    ip_address: str
    status: str
    protocol: str

    @field_validator('ip_address')
    @classmethod
    def check_ip_or_unassigned(cls, value: str) -> str:
        """Ensures the IP is either valid IPv4 or explicitly 'unassigned'."""
        if value.lower() != 'unassigned':
            ipaddress.IPv4Address(value)
        return value


class BGPNeighbor(BaseModel):
    neighbor: str
    asn: int
    up_down: str
    state_pfx: str
    
    @field_validator('neighbor')
    @classmethod
    def check_valid_ip(cls, value: str) -> str:
        """Ensures the neighbor is a valid IPv4 address."""
        ipaddress.IPv4Address(value)
        return value
    
    @field_validator('state_pfx')
    @classmethod
    def check_secure_state(cls, value: str) -> str:
        """
        Audit Rule: If the state is a word (like 'Active' or 'Idle') instead of a 
        prefix number, the BGP peering session is down or failing to establish.
        """
        if value.isalpha() and value.lower() != "established":
            raise ValueError(f"Insecure/Down BGP State detected: '{value}'. Expected numerical prefix count.")
        return value