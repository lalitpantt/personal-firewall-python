import argparse
from pathlib import Path
from typing import List, Optional

from .enforcer import get_enforcer
from .model import Action, Direction, FirewallRule, Protocol
from .storage import RuleStorage


def _parse_enum(value: str, enum_type):
    try:
        return enum_type(value.lower())
    except ValueError:
        allowed = ", ".join(item.value for item in enum_type)
        raise argparse.ArgumentTypeError(f"Expected one of: {allowed}")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Personal Firewall Application CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        default=Path("rules.json"),
        help="Path to the firewall rule store.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List configured firewall rules")
    list_parser.set_defaults(func=list_rules)

    add_parser = subparsers.add_parser("add", help="Add a new firewall rule")
    add_parser.add_argument("--direction", type=lambda value: _parse_enum(value, Direction), required=True)
    add_parser.add_argument("--protocol", type=lambda value: _parse_enum(value, Protocol), required=True)
    add_parser.add_argument("--port", type=int, required=False)
    add_parser.add_argument("--address", type=str, required=False)
    add_parser.add_argument("--action", type=lambda value: _parse_enum(value, Action), required=True)
    add_parser.add_argument("--description", type=str, default="")
    add_parser.set_defaults(func=add_rule)

    remove_parser = subparsers.add_parser("remove", help="Remove a rule by index")
    remove_parser.add_argument("--index", type=int, required=True)
    remove_parser.set_defaults(func=remove_rule)

    apply_parser = subparsers.add_parser("apply", help="Apply rules to the host firewall")
    apply_parser.set_defaults(func=apply_rules)

    return parser


def list_rules(args: argparse.Namespace) -> None:
    storage = RuleStorage(path=args.data_file)
    rules = storage.load_rules()
    if not rules:
        print("No rules defined.")
        return
    for idx, rule in enumerate(rules, start=1):
        port = rule.port or "any"
        address = rule.address or "any"
        print(
            f"{idx}. {rule.action.value.upper()} {rule.direction.value} {rule.protocol.value} "
            f"port={port} address={address} description={rule.description or 'none'}"
        )


def add_rule(args: argparse.Namespace) -> None:
    storage = RuleStorage(path=args.data_file)
    rule = FirewallRule(
        direction=args.direction,
        protocol=args.protocol,
        port=args.port,
        address=args.address,
        action=args.action,
        description=args.description,
    )
    storage.save_rules(storage.load_rules() + [rule])
    print("Rule added successfully.")


def remove_rule(args: argparse.Namespace) -> None:
    storage = RuleStorage(path=args.data_file)
    try:
        storage.remove_rule(args.index - 1)
        print("Rule removed successfully.")
    except IndexError:
        print("Error: Invalid rule index.")


def apply_rules(args: argparse.Namespace) -> None:
    storage = RuleStorage(path=args.data_file)
    enforcer = get_enforcer(storage)
    enforcer.apply_rules(storage.load_rules())


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
