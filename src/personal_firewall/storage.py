import json
from pathlib import Path
from typing import List

from .model import FirewallRule


DEFAULT_RULE_FILE = Path("rules.json")


class RuleStorage:
    def __init__(self, path: Path = DEFAULT_RULE_FILE):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load_rules(self) -> List[FirewallRule]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return [FirewallRule.from_dict(item) for item in data]

    def save_rules(self, rules: List[FirewallRule]) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump([rule.to_dict() for rule in rules], handle, indent=2)
