#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║  Netdiscover++ — Advanced Network Discovery & Reconnaissance Tool        ║
║                                                                          ║
║  ⚠  LEGAL NOTICE:                                                        ║
║  This tool is for AUTHORIZED security testing only. Scanning networks    ║
║  or devices without explicit written permission is ILLEGAL.              ║
║  The author assumes no liability for misuse.                             ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import argparse
import csv
import ipaddress
import json
import os
import socket
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ─── Third-party imports ──────────────────────────────────────────────────
try:
    from scapy.all import ARP, Ether, srp, sniff
except ImportError:
    print("[!] Missing dependency: scapy. Install with: pip install scapy")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.align import Align
    from rich.text import Text
    from rich.progress import (
        Progress, SpinnerColumn, BarColumn,
        TextColumn, TimeElapsedColumn,
    )
except ImportError:
    print("[!] Missing dependency: rich. Install with: pip install rich")
    sys.exit(1)

try:
    import netifaces
except ImportError:
    print("[!] Missing dependency: netifaces. Install with: pip install netifaces")
    sys.exit(1)

try:
    from mac_vendor_lookup import MacLookup
except ImportError:
    print("[!] Missing dependency: mac-vendor-lookup. "
          "Install with: pip install mac-vendor-lookup")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════
#  BANNER
# ═══════════════════════════════════════════════════════════════════════════
console = Console()

BANNER_ART = r"""
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
"""

SUBTITLE = "Advanced Network Discovery & Reconnaissance Tool"
VERSION  = "v1.0.0"
AUTHOR   = "Security Research Project"

LEGAL_WARNING = (
    "[bold red]⚠  LEGAL NOTICE:[/] This tool is intended for "
    "[bold yellow]authorized security testing only[/].\n"
    "   Scanning networks or devices without explicit written permission\n"
    "   is [bold red]illegal[/] and may result in criminal prosecution.\n"
    "   [italic]By continuing, you confirm you have proper authorization.[/]"
)


def print_banner():
    console.print(BANNER_ART, style="bold cyan", highlight=False)
    console.print(Align.center(Text(f"  {SUBTITLE}  ",
                                    style="bold white on blue")))
    console.print(Align.center(Text(f"{VERSION}  •  {AUTHOR}",
                                    style="dim italic")))
    console.print()


def print_legal_warning():
    console.print(Panel(LEGAL_WARNING, title="[bold red]READ BEFORE USE[/]",
                        border_style="red", padding=(1, 2)))
    console.print()


def print_section(title, style="bold green"):
    console.print(f"\n[{style}]▶ {title}[/{style}]")
    console.print(f"[{style}]" + "─" * (len(title) + 2) + f"[/{style}]")


def print_success(msg): console.print(f"[bold green]✔[/] {msg}")
def print_error(msg):   console.print(f"[bold red]✘[/] {msg}")
def print_info(msg):    console.print(f"[bold blue]ℹ[/] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
#  NETWORK UTILITIES
# ═══════════════════════════════════════════════════════════════════════════
def get_interfaces():
    """Return active IPv4 interfaces with subnet info."""
    results = []
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET not in addrs:
            continue
        for addr in addrs[netifaces.AF_INET]:
            ip = addr.get('addr')
            netmask = addr.get('netmask')
            if not ip or ip.startswith('127.'):
                continue
            try:
                net = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                results.append({
                    'name': iface,
                    'ip': ip,
                    'netmask': netmask,
                    'network': str(net),
                    'mac': addrs.get(netifaces.AF_LINK, [{}])[0].get('addr'),
                })
            except Exception:
                continue
    return results


def get_default_interface():
    try:
        return netifaces.gateways()['default'][netifaces.AF_INET][1]
    except (KeyError, IndexError):
        return None


def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════════════
#  VENDOR / DEVICE CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════════════
class VendorResolver:
    def __init__(self):
        self.lookup = MacLookup()
        self._cache = {}
        try:
            self.lookup.update_vendors()
        except Exception:
            pass  # offline / already cached

    def resolve(self, mac):
        if not mac:
            return "Unknown"
        mac = mac.upper()
        if mac in self._cache:
            return self._cache[mac]
        try:
            vendor = self.lookup.lookup(mac)
        except Exception:
            vendor = "Unknown"
        self._cache[mac] = vendor
        return vendor

    @staticmethod
    def classify_device(vendor):
        v = vendor.lower()
        keywords = {
            'Router/Gateway':  ['cisco', 'tp-link', 'netgear', 'd-link',
                                'ubiquiti', 'mikrotik', 'arris', 'zyxel',
                                'linksys', 'tenda'],
            'Camera/IoT':      ['hikvision', 'dahua', 'axis', 'reolink',
                                'amcrest', 'wyze', 'ring', 'nest', 'espressif',
                                'tuya', 'sonoff', 'shelly'],
            'Mobile':          ['apple', 'samsung', 'xiaomi', 'huawei',
                                'oppo', 'vivo', 'oneplus', 'motorola'],
            'Computer':        ['intel', 'dell', 'hp ', 'lenovo', 'asus',
                                'gigabyte', 'msi', 'micro-star', 'acer',
                                'toshiba', 'realtek'],
            'Printer':         ['hewlett', 'canon', 'epson', 'brother',
                                'lexmark', 'xerox'],
            'Virtual Machine': ['vmware', 'virtualbox', 'qemu', 'xensource',
                                'parallels'],
            'Raspberry Pi':    ['raspberry'],
        }
        for role, keys in keywords.items():
            if any(k in v for k in keys):
                return role
        return "Unknown"


# ═══════════════════════════════════════════════════════════════════════════
#  ACTIVE ARP SCANNER
# ═══════════════════════════════════════════════════════════════════════════
class ARPScanner:
    def __init__(self, interface=None, timeout=2, retries=2, threads=20):
        self.interface = interface
        self.timeout = timeout
        self.retries = retries
        self.threads = threads

    def _scan_single(self, ip):
        for _ in range(self.retries):
            try:
                pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
                result = srp(pkt, timeout=self.timeout,
                             iface=self.interface, verbose=False)[0]
                if result:
                    return {'ip': result[0][1].psrc,
                            'mac': result[0][1].hwsrc}
            except Exception:
                continue
        return None

    def scan_range(self, target_range, progress_callback=None):
        network = ipaddress.IPv4Network(target_range, strict=False)
        hosts = [str(ip) for ip in network.hosts()]
        live = []
        done = 0
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = {ex.submit(self._scan_single, ip): ip for ip in hosts}
            for fut in as_completed(futures):
                res = fut.result()
                done += 1
                if res:
                    live.append(res)
                if progress_callback:
                    progress_callback(done, len(hosts), res)
        return live


# ═══════════════════════════════════════════════════════════════════════════
#  PASSIVE SNIFFER
# ═══════════════════════════════════════════════════════════════════════════
class PassiveSniffer:
    def __init__(self, interface=None):
        self.interface = interface
        self.hosts = {}
        self.ip_mac_map = defaultdict(set)
        self.alerts = []

    def _handle(self, pkt):
        if not pkt.haslayer(ARP):
            return
        arp = pkt[ARP]
        ip, mac = arp.psrc, arp.hwsrc
        if ip == "0.0.0.0":
            return
        now = time.time()
        if ip in self.hosts:
            self.hosts[ip]['last_seen'] = now
        else:
            self.hosts[ip] = {'ip': ip, 'mac': mac,
                              'first_seen': now, 'last_seen': now}
        self.ip_mac_map[ip].add(mac)
        if len(self.ip_mac_map[ip]) > 1:
            self.alerts.append({
                'type': 'ARP_SPOOF_SUSPECTED',
                'ip': ip,
                'macs': list(self.ip_mac_map[ip]),
                'timestamp': now,
            })

    def start(self, duration=60):
        sniff(filter="arp", iface=self.interface,
              prn=self._handle, timeout=duration, store=False)
        return list(self.hosts.values()), self.alerts


# ═══════════════════════════════════════════════════════════════════════════
#  PORT PROBER
# ═══════════════════════════════════════════════════════════════════════════
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143,
                443, 445, 554, 1433, 3306, 3389, 5900, 8000,
                8080, 8443, 8888, 37777]

PORT_SERVICES = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
    80: 'HTTP', 110: 'POP3', 139: 'NetBIOS', 143: 'IMAP',
    443: 'HTTPS', 445: 'SMB', 554: 'RTSP(Camera)', 1433: 'MSSQL',
    3306: 'MySQL', 3389: 'RDP', 5900: 'VNC', 8000: 'HTTP-Alt',
    8080: 'HTTP-Proxy', 8443: 'HTTPS-Alt', 37777: 'Dahua-Cam',
}


class PortProber:
    def __init__(self, timeout=0.5, threads=50):
        self.timeout = timeout
        self.threads = threads

    def _probe(self, ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                if s.connect_ex((ip, port)) == 0:
                    return port
        except Exception:
            pass
        return None

    def probe_host(self, ip, ports=None):
        ports = ports or COMMON_PORTS
        open_ports = []
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = [ex.submit(self._probe, ip, p) for p in ports]
            for f in as_completed(futures):
                r = f.result()
                if r:
                    open_ports.append(r)
        return sorted(open_ports)

    @staticmethod
    def guess_services(open_ports):
        return [PORT_SERVICES.get(p, f'Port-{p}') for p in open_ports]


# ═══════════════════════════════════════════════════════════════════════════
#  EXPORTER
# ═══════════════════════════════════════════════════════════════════════════
class Exporter:
    @staticmethod
    def to_json(hosts, filepath):
        with open(filepath, 'w') as f:
            json.dump({
                'scan_time': datetime.now().isoformat(),
                'host_count': len(hosts),
                'hosts': hosts,
            }, f, indent=2, default=str)

    @staticmethod
    def to_csv(hosts, filepath):
        if not hosts:
            return
        fields = ['ip', 'mac', 'vendor', 'device_type',
                  'hostname', 'open_ports', 'services']
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields,
                                    extrasaction='ignore')
            writer.writeheader()
            for h in hosts:
                row = dict(h)
                if isinstance(row.get('open_ports'), list):
                    row['open_ports'] = ','.join(map(str, row['open_ports']))
                if isinstance(row.get('services'), list):
                    row['services'] = ','.join(row['services'])
                writer.writerow(row)


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN LOGIC
# ═══════════════════════════════════════════════════════════════════════════
def enrich_host(host, resolver, probe_ports=False):
    host['vendor'] = resolver.resolve(host.get('mac', ''))
    host['device_type'] = resolver.classify_device(host['vendor'])
    host['hostname'] = resolve_hostname(host['ip'])
    if probe_ports:
        prober = PortProber()
        host['open_ports'] = prober.probe_host(host['ip'])
        host['services'] = prober.guess_services(host['open_ports'])
    return host


def display_results(hosts, title="Discovered Hosts"):
    table = Table(title=f"[bold cyan]{title}[/]",
                  show_lines=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=3)
    table.add_column("IP", style="cyan")
    table.add_column("MAC", style="magenta")
    table.add_column("Vendor", style="green")
    table.add_column("Type", style="yellow")
    table.add_column("Hostname", style="white")
    table.add_column("Ports", style="red")

    for i, h in enumerate(
        sorted(hosts, key=lambda x: tuple(map(int, x['ip'].split('.')))),
        start=1,
    ):
        ports = ",".join(map(str, h.get('open_ports', []))) or "-"
        table.add_row(
            str(i),
            h['ip'],
            h.get('mac', '-'),
            h.get('vendor', '-'),
            h.get('device_type', '-'),
            h.get('hostname') or '-',
            ports,
        )
    console.print(table)


def print_stats(host_count, duration, scanned=0):
    stats = (
        f"[cyan]Hosts Discovered:[/] [bold white]{host_count}[/]    "
        f"[cyan]Network Scanned:[/] [bold white]{scanned}[/]    "
        f"[cyan]Duration:[/] [bold white]{duration:.2f}s[/]"
    )
    console.print(Panel(Align.center(stats), border_style="cyan",
                        padding=(0, 1)))


def print_alerts(alerts):
    if not alerts:
        return
    print_section("Security Alerts", style="bold red")
    for a in alerts:
        console.print(f"  [red]⚠ {a.get('type')}[/] — "
                      f"IP: [yellow]{a.get('ip')}[/] "
                      f"MACs: [yellow]{a.get('macs')}[/]")


def run_active_scan(args, resolver, interface):
    target = args.range
    if not target:
        iface_info = next(
            (i for i in get_interfaces() if i['name'] == interface), None)
        if not iface_info:
            print_error("Could not auto-detect network range. Use -r.")
            sys.exit(1)
        target = iface_info['network']
        print_info(f"Auto-detected range: [bold]{target}[/]")

    print_section(f"Active Scan — {target}")
    print_info(f"Interface: [bold]{interface}[/]  •  "
               f"Threads: [bold]{args.threads}[/]")

    scanner = ARPScanner(interface=interface, threads=args.threads)
    start = time.time()
    total_hosts = len(list(ipaddress.IPv4Network(target,
                                                 strict=False).hosts()))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Scanning network...",
                                 total=total_hosts)

        def cb(done, total, result):
            progress.update(task, completed=done, total=total)
            if result:
                progress.console.print(
                    f"  [green]✔[/] [cyan]{result['ip']}[/] "
                    f"[magenta]{result['mac']}[/]")

        hosts = scanner.scan_range(target, progress_callback=cb)

    duration = time.time() - start
    for h in hosts:
        enrich_host(h, resolver, probe_ports=args.ports)

    console.print()
    display_results(hosts)
    print_stats(len(hosts), duration, scanned=total_hosts)

    if args.json:
        Exporter.to_json(hosts, args.json)
        print_success(f"Results saved to [bold]{args.json}[/]")
    if args.csv:
        Exporter.to_csv(hosts, args.csv)
        print_success(f"Results saved to [bold]{args.csv}[/]")


def run_passive_scan(args, resolver, interface):
    print_section(f"Passive Monitoring — {args.timeout}s")
    print_info(f"Interface: [bold]{interface}[/]  •  "
               "Listening for ARP traffic...")

    sniffer = PassiveSniffer(interface=interface)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[yellow]Sniffing...", total=None)
        hosts, alerts = sniffer.start(duration=args.timeout)
        progress.update(task, completed=True)

    for h in hosts:
        enrich_host(h, resolver)

    console.print()
    if hosts:
        display_results(hosts, "Passively Discovered Hosts")
    else:
        print_info("No hosts detected during passive monitoring.")
    print_stats(len(hosts), args.timeout)
    print_alerts(alerts)


def build_argparser():
    p = argparse.ArgumentParser(
        prog="netdiscover_plus",
        description="Netdiscover++ — Advanced network discovery tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="⚠  For authorized security testing only.",
    )
    p.add_argument('-i', '--interface', help='Network interface')
    p.add_argument('-r', '--range',
                   help='Target range (e.g., 192.168.1.0/24)')
    p.add_argument('-p', '--passive', action='store_true',
                   help='Passive mode (sniff only)')
    p.add_argument('-t', '--timeout', type=int, default=60,
                   help='Passive mode duration in seconds (default: 60)')
    p.add_argument('--ports', action='store_true',
                   help='Enable port scanning (slower)')
    p.add_argument('--json', help='Export results to JSON file')
    p.add_argument('--csv', help='Export results to CSV file')
    p.add_argument('--threads', type=int, default=20,
                   help='Number of scanning threads (default: 20)')
    p.add_argument('--no-banner', action='store_true',
                   help='Skip banner display')
    p.add_argument('--skip-legal', action='store_true',
                   help='Skip legal warning (for lab environments)')
    return p


def main():
    args = build_argparser().parse_args()

    if not args.no_banner:
        print_banner()
    if not args.skip_legal:
        print_legal_warning()

    if os.geteuid() != 0:
        print_error("Raw sockets require root. Run with sudo.")
        sys.exit(1)

    resolver = VendorResolver()
    interface = args.interface or get_default_interface()
    if not interface:
        print_error("No active network interface found.")
        sys.exit(1)

    print_info(f"Using interface: [bold]{interface}[/]")

    try:
        if args.passive:
            run_passive_scan(args, resolver, interface)
        else:
            run_active_scan(args, resolver, interface)
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ Scan interrupted by user.[/]")
        sys.exit(0)
    except PermissionError:
        print_error("Permission denied. Run with sudo.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

    console.print()
    print_success("Scan complete.")


if __name__ == '__main__':
    main()