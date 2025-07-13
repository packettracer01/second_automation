# OSPF Automation with Python & Netmiko

This project automates the configuration of **OSPF (Open Shortest Path First)** routing across multiple **Cisco routers** hosted on an **EVE-NG lab environment**. Using Python and the Netmiko library, the script assigns IP addresses to interfaces, configures OSPF (in Area 0), saves the configuration, and verifies routing by displaying OSPF neighbors and the OSPF database.

## 🚀 Features

- Connects to routers via SSH using secure credential prompts (`getpass`)
- Configures multiple router interfaces with specified IPs and subnet masks
- Automatically calculates wildcard masks for OSPF configuration
- Configures `router ospf 1` in Area 0
- Saves running configuration to memory (`write memory`)
- Verifies routing with:
  - `show ip ospf neighbor`
  - `show ip ospf database`

## 📁 Project Structure

``
