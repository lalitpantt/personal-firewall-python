# Personal Firewall Application

## Overview

This project delivers a professional, extensible personal firewall solution with a clean architecture and cross-platform support.

It is designed to demonstrate core concepts in system-level security, network filtering, and rule-based traffic control.

## Objective

Design and implement a personal firewall application capable of monitoring and filtering inbound and outbound traffic.

## Key Features

- Rule-based traffic control for incoming and outgoing connections
- Protocol-aware packet handling for TCP, UDP, and ICMP
- Linux `iptables` integration for production filtering
- Windows WinAPI support scaffold for future native implementation
- Secure architecture with configuration-driven rule management

## Technologies

- Python 3.11+
- Linux `iptables`
- Windows WinAPI (platform abstraction layer)

## Project Structure

- `src/personal_firewall/` — application source code
- `pyproject.toml` — packaging metadata
- `README.md` — project overview and usage
- `.gitignore` — ignored files for version control

## Usage

```bash
python -m personal_firewall --help
```

### Example commands

- List configured firewall rules
  ```bash
  python -m personal_firewall list
  ```

- Add a new allow rule for outbound TCP port 443
  ```bash
  python -m personal_firewall add --direction outbound --protocol tcp --port 443 --action allow
  ```

- Remove an existing rule by its index
  ```bash
  python -m personal_firewall remove --index 1
  ```

## Design Principles

- Modular platform abstraction for Linux and Windows
- Simple CLI for management and inspection
- Clear separation between rule models and enforcement layer
- Safe defaults and non-destructive behavior on unsupported platforms
# personal-firewall-python
