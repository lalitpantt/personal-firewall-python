from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Action(Enum):
    ALLOW = "allow"
    DENY = "deny"


class Direction(Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"


@dataclass
class FirewallRule:
    direction: Direction
    protocol: Protocol
    port: Optional[int]
    address: Optional[str]
    action: Action
    description: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "direction": self.direction.value,
            "protocol": self.protocol.value,
            "port": self.port,
            "address": self.address,
            "action": self.action.value,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FirewallRule":
        return cls(
            direction=Direction(data["direction"]),
            protocol=Protocol(data["protocol"]),
            port=data.get("port"),
            address=data.get("address"),
            action=Action(data["action"]),
            description=data.get("description"),
        )
