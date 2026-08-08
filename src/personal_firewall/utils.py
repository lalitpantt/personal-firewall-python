from typing import List


def format_rule(rule) -> str:
    port = rule.port if rule.port is not None else "any"
    address = rule.address or "any"
    return f"{rule.action.value.upper()} {rule.direction.value} {rule.protocol.value} port={port} address={address}"


def validate_port(port: int) -> bool:
    return 0 < port <= 65535
