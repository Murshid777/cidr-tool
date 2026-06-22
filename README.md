<h1 align="center">
  🔍 CIDR Tool
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-cyan?style=for-the-badge&logo=opensourceinitiative&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Made%20by-Murshid-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-yellow?style=for-the-badge"/>
</p>

<p align="center">
  A stylish, interactive CIDR IP Range Analyzer for pentesters and security researchers.<br>
  Inspired by the design of <b>Sublist3r</b>.
</p>

---

## 🖼️ Preview

```
  ██████╗██╗██████╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     
 ██╔════╝██║██╔══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
 ██║     ██║██║  ██║██████╔╝       ██║   ██║   ██║██║   ██║██║     
 ██║     ██║██║  ██║██╔══██╗       ██║   ██║   ██║██║   ██║██║     
 ╚██████╗██║██████╔╝██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
  ╚═════╝╚═╝╚═════╝ ╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝

  ─────────────────────────────────────────────────────────────────
            [*] CIDR IP Range Analyzer
            [*] Platform : Windows |Linux 
  ─────────────────────────────────────────────────────────────────
            ╔═══════════════════════════════════╗
            ║  ⚡ Powered by  Murshid  ⚡  ║
            ╚═══════════════════════════════════╝
  ─────────────────────────────────────────────────────────────────

  [~] Scanning target CIDR...
  [████████████████████████████████████████] 100%

  [*] Network Information
  ──────────────────────────────────────────────────────
  Target CIDR              →  192.168.1.0/24
  Network ID               →  192.168.1.0
  Broadcast Address        →  192.168.1.255
  Subnet Mask              →  255.255.255.0
  Binary Subnet Mask       →  11111111.11111111.11111111.00000000
  Wildcard Mask            →  0.0.0.255
  Prefix Length            →  /24
  IP Version               →  IPv4
  CIDR Class               →  Class C  (192.0.0.0 – 223.255.255.255)

  [*] Host Range
  ──────────────────────────────────────────────────────
  Total IPs                →  256
  Usable Hosts             →  254
  First Host               →  192.168.1.1
  Last Host                →  192.168.1.254

  [+] Done!⚡
```

---

## ⚡ Features

| Feature | Description |
|---|---|
| 🎨 Stylish UI | Sublist3r-inspired terminal design with colors |
| 📊 Progress Bar | Animated progress bar while scanning |
| 🌐 Network Info | Network ID, Broadcast, Subnet, Wildcard mask |
| 🔢 Binary Subnet | Shows subnet mask in binary format |
| 🏷️ CIDR Class | Auto-detects Class A / B / C / D / Loopback |
| 🔗 /31 & /32 Support | RFC 3021 compliant point-to-point & single host |
| 🛡️ IPv6 Blocked | IPv4 only — prevents memory crash |
| 💾 Save to File | Export host list for Nmap, ffuf, etc. |
| ⚠️ Overwrite Warning | Warns before overwriting existing files |
| 🔁 Scan Again | Scan multiple CIDRs in one session |
| 🧠 Input Validation | Handles empty input, bad y/n, missing prefix |
| 🚨 Error Handling | Permission, disk full, directory errors caught |

---

## 🛠️ Installation

## 🪟 Windows Usage

### Install Python Dependency

Open **Command Prompt** or **PowerShell**:

```powershell
pip install -r requirements.txt
```

Or install the required package manually:

```powershell
pip install termcolor
```

### Run the Tool

```powershell
python cidr.py
```

If multiple Python versions are installed:

```powershell
py cidr.py
```

### Example

```powershell
C:\cidr-tool> python cidr.py

[?] Enter CIDR (e.g. 192.168.1.0/24) : 192.168.1.0/24
[?] Save host list to file? (y/n)     : y
[?] Output filename                   : targets.txt
[?] Show all usable hosts? (y/n)      : n
```

### Use Output with Nmap

```powershell
python cidr.py
nmap -iL targets.txt
```

### Common Issues

| Issue                            | Fix                                                            |
| -------------------------------- | -------------------------------------------------------------- |
| `'python' is not recognized`     | Reinstall Python and enable **Add Python to PATH**             |
| `ModuleNotFoundError: termcolor` | Run `pip install termcolor`                                    |
| Permission denied when saving    | Run Command Prompt as Administrator or choose another folder   |
| Colored text not displaying      | Use Windows Terminal, PowerShell 7+, or Windows 10/11 Terminal |

```
```


```bash
# Clone the repo
git clone https://github.com/Murshid777/cidr-tool.git
cd cidr-tool

# Install dependency
pip install -r requirements.txt --break-system-packages
```

Or via apt:
```bash
sudo apt install python3-termcolor -y
```

---

## 🚀 Usage

```bash
python3 cidr.py
```

Follow the interactive prompts:

```
[?] Enter CIDR (e.g. 192.168.1.0/24) : 192.168.1.0/24
[?] Save host list to file? (y/n)     : y
[?] Output filename                   : targets.txt
[?] Show all usable hosts? (y/n)      : n
```

**Pipe to Nmap:**
```bash
python3 cidr.py   # save to targets.txt
nmap -iL targets.txt
```

---

## 🧪 Tested Inputs

| Input | Result |
|---|---|
| `192.168.1.0/24` | ✅ Normal scan |
| `10.0.0.0/8` | ✅ Large network — listing disabled, save works |
| `192.168.1.0/31` | ✅ RFC 3021 P2P — Host A & B shown |
| `192.168.1.1/32` | ✅ Single host |
| `172.16.50.04/24` | ✅ Leading zero auto-fixed → `172.16.50.4/24` |
| `2001:db8::/32` | ✅ Blocked — IPv4 only |
| ` ` (empty) | ✅ Re-prompts with error |
| `192.168.1.0` (no prefix) | ✅ Re-prompts with error |

---

## 📁 File Structure

```
cidr-tool/
├── cidr.py       # Main script
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
└── README.md           # This file
```

---

## 📦 Requirements

| Package | Version |
|---|---|
| Python | 3.6+ |
| termcolor | 1.1.0+ |

---

## 👤 Author

**Murshid**
- Offensive Security Enthusiast
- Platforms: HackTheBox · TryHackMe · Bugcrowd
- Working toward: eJPT → PNPT → OSCP

---

## 📜 License

This project is licensed under the [MIT License](LICENSE) — free to use, modify, and distribute.

---

<p align="center">Made with ❤️ by Murshid &nbsp;|&nbsp;⚡</p>
