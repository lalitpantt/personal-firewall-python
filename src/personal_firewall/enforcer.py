import platform
from typing import List

from .model import FirewallRule
from .storage import RuleStorage


class BaseEnforcer:
    def __init__(self, storage: RuleStorage):
        self.storage = storage

    def apply_rules(self, rules: List[FirewallRule]) -> None:
        raise NotImplementedError("Platform-specific enforcers must implement apply_rules")

    def list_rules(self) -> List[FirewallRule]:
        return self.storage.load_rules()

    def add_rule(self, rule: FirewallRule) -> None:
        rules = self.storage.load_rules()
        rules.append(rule)
        self.storage.save_rules(rules)

    def remove_rule(self, index: int) -> None:
        rules = self.storage.load_rules()
        if index < 0 or index >= len(rules):
            raise IndexError("Rule index out of range")
        del rules[index]
        self.storage.save_rules(rules)


class LinuxEnforcer(BaseEnforcer):
    def apply_rules(self, rules: List[FirewallRule]) -> None:
        print("[LinuxEnforcer] Applying rules through iptables integration")
        for rule in rules:
            print(f"- {rule}")
        # Real iptables integration can be added here.


class WindowsEnforcer(BaseEnforcer):
    def apply_rules(self, rules: List[FirewallRule]) -> None:
        print("[WindowsEnforcer] Applying rules through WinAPI integration")
        for rule in rules:
            print(f"- {rule}")
        # Real WinAPI integration can be added here.


def get_enforcer(storage: RuleStorage) -> BaseEnforcer:
    current = platform.system().lower()
    if current == "linux":
        return LinuxEnforcer(storage)
    if current == "windows":
        return WindowsEnforcer(storage)
    return BaseEnforcer(storage)
