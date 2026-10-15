<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!--                         NETDISCOVER++ README                            -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

<div align="center">

<!-- ╔══════════════════════════════════════════════════════════════════════╗ -->
<!-- ║                          ASCII BANNER                                ║ -->
<!-- ╚══════════════════════════════════════════════════════════════════════╝ -->

```
 ███▄    █ ▓█████▄  ██▓  ██████  ▄████▄   ▒█████   ██▒   █▓▓█████  ██▀███
 ██ ▀█   █ ▒██▀ ██▌▓██▒▒██    ▒ ▒██▀ ▀█  ▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒
▓██  ▀█ ██▒░██   █▌▒██▒░ ▓██▄   ▒▓█    ▄ ▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒
▓██▒  ▐▌██▒░▓█▄   ▌░██░  ▒   ██▒▒▓▓▄ ▄██▒▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄
▒██░   ▓██░░▒████▓ ░██░▒██████▒▒▒ ▓███▀ ░░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒
░ ▒░   ▒ ▒  ▒▒▓  ▒ ░▓  ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░░   ░ ▒░ ░ ▒  ▒  ▒ ░░ ░▒  ░ ░  ░  ▒     ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░
   ░   ░ ░  ░ ░  ░  ▒ ░░  ░  ░  ░        ░ ░ ░ ▒       ░░     ░     ░░   ░
         ░    ░     ░        ░  ░ ░          ░ ░        ░     ░  ░   ░
                                ░                      ░
```

### 🛰️ Advanced Network Discovery & Reconnaissance Tool

**ARP Scanning** • **Passive Sniffing** • **MAC Vendor Lookup** • **Port Probing**

<br>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!--                               BADGES                                    -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Kali](https://img.shields.io/badge/Kali-2023%2B-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

![Scapy](https://img.shields.io/badge/Built%20with-Scapy-00A3E0?style=flat-square)
![Rich](https://img.shields.io/badge/UI-Rich-FF6B6B?style=flat-square)
![Root](https://img.shields.io/badge/Requires-Root%20%2F%20Sudo-critical?style=flat-square)

<br>

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!--                          LEGAL WARNING                                  -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

> ### ⚠️ LEGAL NOTICE
> **This tool is intended for authorized security testing only.**
> Scanning networks or devices without explicit written permission is **illegal** and may result in criminal prosecution. The author assumes **no liability** for misuse.

</div>

---

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!--                          TABLE OF CONTENTS                              -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

<div align="center">

## 📖 Table of Contents

[✨ Features](#-features) •
[📋 Requirements](#-requirements) •
[⚡ Quick Install](#-one-line-installation-kali-linux) •
[📦 Manual Install](#-manual-installation) •
[🐍 Virtual Env](#-virtual-environment-recommended) •
[📚 Usage](#-usage) •
[🖥️ Sample Output](#️-sample-output) •
[🐛 Troubleshooting](#-troubleshooting) •
[🗑️ Uninstall](#️-uninstall)

</div>

---

<div align="center">

## ⚡ One-Line Installation (Kali Linux)

</div>

```bash
sudo apt update && sudo apt install -y python3 python3-pip libpcap-dev git && sudo pip3 install --break-system-packages scapy rich netifaces mac-vendor-lookup && git clone https://github.com/<your-username>/netdiscover-plus.git && cd netdiscover-plus && chmod +x netdiscover_plus.py && sudo cp netdiscover_plus.py /usr/local/bin/netdiscover-plus && sudo chmod +x /usr/local/bin/netdiscover-plus && echo "✅ Installation complete. Run: sudo netdiscover-plus -r <range> -i <iface>"
```

### 🚀 Run it

```bash
sudo netdiscover-plus -r 192.168.1.0/24 -i eth0
```

---

## 📦 Manual Installation

```bash
# ── Step 1: Update package lists ──────────────────────────────────────────
sudo apt update

# ── Step 2: Install system dependencies ───────────────────────────────────
sudo apt install -y python3 python3-pip libpcap-dev git

# ── Step 3: Install Python dependencies ───────────────────────────────────
sudo pip3 install --break-system-packages scapy rich netifaces mac-vendor-lookup

# ── Step 4: Clone the repository ──────────────────────────────────────────
git clone https://github.com/<your-username>/netdiscover-plus.git
cd netdiscover-plus

# ── Step 5: Make executable ───────────────────────────────────────────────
chmod +x netdiscover_plus.py

# ── Step 6: (Optional) Install globally ───────────────────────────────────
sudo cp netdiscover_plus.py /usr/local/bin/netdiscover-plus
sudo chmod +x /usr/local/bin/netdiscover-plus
```

---

## 🐍 Virtual Environment (Recommended)

```bash
# ── Step 1: System deps ───────────────────────────────────────────────────
sudo apt update && sudo apt install -y python3-venv libpcap-dev git

# ── Step 2: Clone repo ────────────────────────────────────────────────────
git clone https://github.com/<your-username>/netdiscover-plus.git
cd netdiscover-plus

# ── Step 3: Create & activate venv ────────────────────────────────────────
python3 -m venv venv
source venv/bin/activate

# ── Step 4: Install dependencies ──────────────────────────────────────────
pip install --upgrade pip
pip install scapy rich netifaces mac-vendor-lookup

# ── Step 5: Run (sudo with explicit venv python) ──────────────────────────
sudo ./venv/bin/python netdiscover_plus.py -r 192.168.1.0/24 -i eth0
```

> 💡 **Tip:** To let `sudo` keep your venv active, add this to `/etc/sudoers.d/venv`:
> ```
> Defaults env_keep += "VIRTUAL_ENV PATH"
> ```

---

## 📋 Requirements

<table align="center">
<tr>
<th>Component</th>
<th>Minimum</th>
</tr>
<tr>
<td>🐍 Python</td>
<td><b>3.8+</b></td>
</tr>
<tr>
<td>🐧 OS</td>
<td>Kali Linux (also Debian / Ubuntu)</td>
</tr>
<tr>
<td>🔑 Privileges</td>
<td><b>root / sudo</b> (raw sockets)</td>
</tr>
<tr>
<td>📚 Libraries</td>
<td><code>libpcap-dev</code></td>
</tr>
</table>

### Python Packages

| 📦 Package | 🎯 Purpose |
|---|---|
| `scapy` | Packet crafting & sniffing |
| `rich` | Terminal UI |
| `netifaces` | Interface enumeration |
| `mac-vendor-lookup` | OUI vendor database |

---

## ✨ Features

<table align="center">
<tr>
<td>🔍 <b>Active ARP Scan</b></td>
<td>Multi-threaded host discovery across a CIDR range</td>
</tr>
<tr>
<td>👂 <b>Passive Sniffing</b></td>
<td>Silently observe ARP traffic on the wire</td>
</tr>
<tr>
<td>🏷️ <b>MAC Vendor Lookup</b></td>
<td>Identifies hardware vendor from OUI</td>
</tr>
<tr>
<td>🖥️ <b>Device Classification</b></td>
<td>Router, IoT, Mobile, Printer, VM, etc.</td>
</tr>
<tr>
<td>🔌 <b>Port Probing</b></td>
<td>Optional TCP scan of common ports + service guessing</td>
</tr>
<tr>
<td>🚨 <b>ARP Spoof Detection</b></td>
<td>Alerts on IP→multiple MAC anomalies</td>
</tr>
<tr>
<td>📊 <b>Rich Terminal UI</b></td>
<td>Colored tables, live progress bars, stats panels</td>
</tr>
<tr>
<td>💾 <b>Export</b></td>
<td>Save results to JSON or CSV</td>
</tr>
</table>

---

## 📚 Usage

```
usage: netdiscover-plus [-h] [-i INTERFACE] [-r RANGE] [-p]
                        [-t TIMEOUT] [--ports] [--json JSON]
                        [--csv CSV] [--threads THREADS]
                        [--no-banner] [--skip-legal]
```

<table align="center">
<tr>
<th>Flag</th>
<th>Description</th>
</tr>
<tr><td><code>-i, --interface</code></td><td>Network interface (default: auto-detected)</td></tr>
<tr><td><code>-r, --range</code></td><td>Target CIDR range (default: auto-detected)</td></tr>
<tr><td><code>-p, --passive</code></td><td>Passive mode — sniff only, no probes</td></tr>
<tr><td><code>-t, --timeout</code></td><td>Passive duration in seconds (default: <code>60</code>)</td></tr>
<tr><td><code>--ports</code></td><td>Enable TCP port probing (slower)</td></tr>
<tr><td><code>--json FILE</code></td><td>Export results to JSON</td></tr>
<tr><td><code>--csv FILE</code></td><td>Export results to CSV</td></tr>
<tr><td><code>--threads N</code></td><td>Number of scanning threads (default: <code>20</code>)</td></tr>
<tr><td><code>--no-banner</code></td><td>Skip the ASCII banner</td></tr>
<tr><td><code>--skip-legal</code></td><td>Skip legal warning (lab use only)</td></tr>
</table>

### 💡 Examples

```bash
# Active scan of a subnet
sudo netdiscover-plus -r 192.168.1.0/24 -i eth0

# Auto-detect range & scan with port probing
sudo netdiscover-plus -i eth0 --ports --json scan.json

# Passive monitoring for 5 minutes
sudo netdiscover-plus -p -i eth0 -t 300

# Quiet scan for scripting / automation
sudo netdiscover-plus -r 10.0.0.0/24 --no-banner --skip-legal --csv out.csv
```

---

## 🖥️ Sample Output

```
▶ Active Scan — 192.168.1.0/24
──────────────────────────────
ℹ Interface: eth0  •  Threads: 20

  ✔ 192.168.1.1     aa:bb:cc:11:22:33
  ✔ 192.168.1.12    de:ad:be:ef:00:01
  ✔ 192.168.1.45    f0:18:98:aa:bb:cc

         Discovered Hosts
┏━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━┓
┃ # ┃ IP            ┃ MAC               ┃ Vendor    ┃ Type    ┃ Hostname┃ Ports┃
┡━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━┩
│ 1 │ 192.168.1.1   │ aa:bb:cc:11:22:33 │ TP-Link   │ Router  │ router  │ 80   │
│ 2 │ 192.168.1.12  │ de:ad:be:ef:00:01 │ Raspberry │ RPi     │ pi-hole │ 22,80│
│ 3 │ 192.168.1.45  │ f0:18:98:aa:bb:cc │ Apple     │ Mobile  │ -       │ -    │
└───┴───────────────┴───────────────────┴───────────┴─────────┴─────────┴──────┘

╭──────────────────────────────────────────────╮
│ Hosts Discovered: 3   Network Scanned: 254   │
│ Duration: 2.14s                              │
╰──────────────────────────────────────────────╯
```

---

## ✅ Verify Installation

```bash
# Check help output loads
sudo netdiscover-plus --help

# Quick smoke test
sudo netdiscover-plus -i eth0 --no-banner --skip-legal
```

---

## 🐛 Troubleshooting

<table align="center">
<tr>
<th>⚠️ Error</th>
<th>✅ Fix</th>
</tr>
<tr><td><code>Raw sockets require root</code></td><td>Prefix command with <code>sudo</code></td></tr>
<tr><td><code>No active network interface found</code></td><td>Pass <code>-i &lt;iface&gt;</code> explicitly</td></tr>
<tr><td><code>ModuleNotFoundError: netifaces</code></td><td><code>sudo pip3 install --break-system-packages netifaces</code></td></tr>
<tr><td><code>ModuleNotFoundError: scapy</code></td><td><code>sudo pip3 install --break-system-packages scapy</code></td></tr>
<tr><td><code>PermissionError</code> on sniff</td><td>Install <code>libpcap-dev</code>, run as root</td></tr>
<tr><td><code>error: externally-managed-environment</code></td><td>Add <code>--break-system-packages</code> or use venv</td></tr>
<tr><td>Slow scan</td><td>Adjust <code>--threads</code>; lower on congested LANs</td></tr>
<tr><td>Empty results</td><td>Verify subnet; try <code>-r &lt;your-subnet&gt;</code></td></tr>
<tr><td><code>netifaces</code> build fails</td><td><code>pip install netifaces --no-binary :all:</code></td></tr>
</table>

### 🔍 Find your interface name

```bash
ip a
# Common: eth0, wlan0, ens33 (VMs), wlp3s0 (WiFi)
```

---

## 🗑️ Uninstall

```bash
# Remove global command
sudo rm /usr/local/bin/netdiscover-plus

# Remove Python packages (only if unused elsewhere)
sudo pip3 uninstall scapy rich netifaces mac-vendor-lookup

# Remove cloned repo
rm -rf ~/netdiscover-plus
```

---

## 📄 License

Released for **educational and authorized security testing** purposes only.
The author assumes **no responsibility** for misuse or damage caused by this tool.

---

## 🔗 Related Tools

<table align="center">
<tr>
<td align="center" width="25%">
<a href="https://github.com/royhills/arp-scan">
<b>arp-scan</b><br>
<sub>Classic ARP scanner</sub>
</a>
</td>
<td align="center" width="25%">
<a href="https://github.com/netdiscover-scanner/netdiscover">
<b>netdiscover</b><br>
<sub>Passive/active ARP tool</sub>
</a>
</td>
<td align="center" width="25%">
<a href="https://nmap.org/">
<b>nmap</b><br>
<sub>Full-featured port scanner</sub>
</a>
</td>
<td align="center" width="25%">
<a href="https://www.bettercap.org/">
<b>bettercap</b><br>
<sub>MITM & recon framework</sub>
</a>
</td>
</tr>
</table>

---

<div align="center">

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!--                              FOOTER                                     -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║         ⚠  Scan only what you own or have written permission        ║
║                                                                      ║
║              You are responsible for how you use this tool           ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Made with 🛰️ for the security community**

⭐ If this tool helped you, consider giving it a star!

<br>

<sub>Netdiscover++ © 2024 — Educational & Authorized Testing Only</sub>

</div>
