#!/usr/bin/env python3

import ipaddress
import sys
import os
import time
from termcolor import colored

BANNER = r"""
  ██████╗██╗██████╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     
 ██╔════╝██║██╔══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
 ██║     ██║██║  ██║██████╔╝       ██║   ██║   ██║██║   ██║██║     
 ██║     ██║██║  ██║██╔══██╗       ██║   ██║   ██║██║   ██║██║     
 ╚██████╗██║██████╔╝██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
  ╚═════╝╚═╝╚═════╝ ╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.02):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def progress_bar(label="Analyzing", duration=1.2, width=40):
    print()
    print(colored(f"  [~] {label}", 'cyan', attrs=['bold']))
    steps = width
    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        filled  = "█" * i
        empty   = "░" * (steps - i)
        bar_str = colored(f"  [", 'cyan') + \
                  colored(filled, 'green', attrs=['bold']) + \
                  colored(empty, 'white') + \
                  colored(f"] ", 'cyan') + \
                  colored(f"{percent}%", 'yellow', attrs=['bold'])
        print(f"\r{bar_str}", end='', flush=True)
        time.sleep(duration / steps)
    print()
    print()

def print_banner():
    clear()
    print(colored(BANNER, 'cyan', attrs=['bold']))
    print(colored("  ─────────────────────────────────────────────────────────────────", 'cyan'))
    slow_print(colored("                [*]  CIDR IP Range Analyzer ", 'yellow', attrs=['bold']))
    slow_print(colored("                [*]  Platform : Windows | Linux  ", 'yellow', attrs=['bold']))
    print(colored("  ─────────────────────────────────────────────────────────────────", 'cyan'))
    print(colored("            ╔═══════════════════════════════════╗", 'cyan'))
    print(colored("            ║ ║ ⚡ ", 'cyan'), end='')
    print(colored("Powered by ", 'white', attrs=['bold']), end='')
    print(colored("M", 'cyan',     attrs=['bold']), end='')
    print(colored("u", 'cyan',  attrs=['bold']), end='')
    print(colored("r", 'cyan',   attrs=['bold']), end='')
    print(colored("s", 'cyan',    attrs=['bold']), end='')
    print(colored("h", 'cyan', attrs=['bold']), end='')
    print(colored("i", 'cyan',  attrs=['bold']), end='')
    print(colored("d", 'cyan',     attrs=['bold']), end='')
    print(colored("  ⚡ ║", 'cyan'))
    print(colored("            ╚═══════════════════════════════════╝", 'cyan'))
    print(colored("  ─────────────────────────────────────────────────────────────────\n", 'cyan'))
    time.sleep(0.3)

def print_section(title):
    print(colored(f"\n  [*] {title}", 'cyan', attrs=['bold']))
    print(colored("  " + "─" * 50, 'cyan'))

def print_row(label, value, color='white'):
    label_str = colored(f"  {label:<26}", 'blue', attrs=['bold'])
    arrow     = colored("→", 'cyan', attrs=['bold'])
    value_str = colored(str(value), color, attrs=['bold'])
    print(f"{label_str} {arrow}  {value_str}")

def get_cidr_class(network):
    first_octet = int(str(network.network_address).split('.')[0])
    if first_octet == 0:
        return "Special (0.x.x.x)"
    elif 1 <= first_octet <= 126:
        return "Class A  (1.0.0.0 – 126.255.255.255)"
    elif first_octet == 127:
        return "Loopback (127.x.x.x)"
    elif 128 <= first_octet <= 191:
        return "Class B  (128.0.0.0 – 191.255.255.255)"
    elif 192 <= first_octet <= 223:
        return "Class C  (192.0.0.0 – 223.255.255.255)"
    elif 224 <= first_octet <= 239:
        return "Class D  (Multicast)"
    else:
        return "Class E  (Reserved / Experimental)"

def to_binary_mask(netmask):
    octets = str(netmask).split('.')
    binary_octets = [f"{int(o):08b}" for o in octets]
    return '.'.join(binary_octets)

def fix_leading_zeros(cidr):
    """172.16.50.04/24 → 172.16.50.4/24"""
    try:
        ip_part, prefix = cidr.split('/')
        cleaned = '.'.join(str(int(o)) for o in ip_part.split('.'))
        return f"{cleaned}/{prefix.strip()}"
    except Exception:
        return cidr

def ask_yn(prompt):
    """Loop until user enters y or n."""
    while True:
        ans = input(colored(prompt, 'yellow', attrs=['bold'])).strip().lower()
        if ans in ('y', 'n'):
            return ans
        print(colored("  [!] Please enter y or n.\n", 'red', attrs=['bold']))

def get_input():
    # ── CIDR input ─────────────────────────────────────────────
    while True:
        print(colored("  ┌──────────────────────────────────────────────────────────────", 'cyan'))
        cidr = input(colored("  │  [?] Enter CIDR (e.g. 192.168.1.0/24) : ", 'green', attrs=['bold'])).strip()
        print(colored("  └──────────────────────────────────────────────────────────────\n", 'cyan'))
        if not cidr:
            print(colored("  [!] Input cannot be empty. Please enter a valid CIDR.\n", 'red', attrs=['bold']))
            continue
        if '/' not in cidr:
            print(colored("  [!] Missing prefix length — e.g. 192.168.1.0/24\n", 'red', attrs=['bold']))
            continue
        cidr = fix_leading_zeros(cidr)
        # Validate prefix range before anything else
        try:
            prefix = int(cidr.split('/')[1])
            if prefix < 1 or prefix > 32:
                print(colored(f"  [!] Invalid prefix /{prefix} — must be between /1 and /32.\n", 'red', attrs=['bold']))
                print(colored(f"  [?] /0 = entire internet (4B IPs) — not a valid scan target.\n", 'yellow'))
                continue
        except ValueError:
            print(colored("  [!] Prefix must be a number — e.g. 192.168.1.0/24\n", 'red', attrs=['bold']))
            continue
        break

    # ── Save to file ────────────────────────────────────────────
    save_file = None
    if ask_yn("  [?] Save host list to file? (y/n)      : ") == 'y':
        while True:
            save_file = input(colored("  [?] Output filename (e.g. hosts.txt)   : ", 'yellow', attrs=['bold'])).strip()
            if not save_file:
                print(colored("  [!] Filename cannot be empty.\n", 'red', attrs=['bold']))
                continue
            if os.path.exists(save_file):
                print()
                print(colored(f"  ⚠️  Warning: '{save_file}' already exists!", 'red', attrs=['bold']))
                if ask_yn("  [?] Overwrite? (y/n)                   : ") == 'y':
                    break
                else:
                    print(colored("  [~] Enter a different filename.\n", 'cyan'))
                    continue
            break

    # ── Show all hosts ──────────────────────────────────────────
    list_hosts = ask_yn("  [?] Show all usable hosts?   (y/n)      : ") == 'y'

    return cidr, list_hosts, save_file

def analyze_cidr(cidr, list_hosts=False, save_file=None):
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError as e:
        print(colored(f"\n  [!] Invalid CIDR notation: {e}\n", 'red', attrs=['bold']))
        return False

    if network.version == 6:
        print(colored("\n  [!] IPv6 is not supported. Please enter an IPv4 CIDR only.\n", 'red', attrs=['bold']))
        return False

    # Safety threshold — /16 পর্যন্ত host list safe (65534 IPs = ~1MB RAM, 0.02s)
    SAFE_THRESHOLD = 65536

    progress_bar("Scanning target CIDR...", duration=1.2)

    binary_mask = to_binary_mask(network.netmask)
    cidr_class  = get_cidr_class(network)
    prefix      = network.prefixlen

    # ── Special cases ──────────────────────────────────────────
    # /32 → single host
    if prefix == 32:
        usable     = 1
        first_host = network.network_address
        last_host  = network.network_address
        large_net  = False
        special    = "single"
    # /31 → point-to-point (RFC 3021) — both IPs usable, no broadcast
    elif prefix == 31:
        usable     = 2
        first_host = network.network_address
        last_host  = network.broadcast_address
        large_net  = False
        special    = "p2p"
    else:
        usable     = max(network.num_addresses - 2, 0)
        large_net  = network.num_addresses > SAFE_THRESHOLD
        first_host = next(network.hosts(), None)
        last_host  = network.broadcast_address - 1 if usable > 0 else None
        special    = None

    print_section("Network Information")
    print_row("Target CIDR",         cidr,                         'green')
    print_row("Network ID",          network.network_address,      'green')

    if prefix == 31:
        print_row("Broadcast Address", "None (RFC 3021 — P2P link)", 'yellow')
    elif prefix == 32:
        print_row("Broadcast Address", "None (single host)",          'yellow')
    else:
        print_row("Broadcast Address", network.broadcast_address,    'red')

    print_row("Subnet Mask",         network.netmask,              'yellow')
    print_row("Binary Subnet Mask",  binary_mask,                  'yellow')
    print_row("Wildcard Mask",       network.hostmask,             'yellow')
    print_row("Prefix Length",       f"/{prefix}",                 'magenta')
    print_row("IP Version",          f"IPv{network.version}",      'cyan')
    print_row("CIDR Class",          cidr_class,                   'magenta')

    print_section("Host Range")
    print_row("Total IPs",           network.num_addresses,        'white')

    if special == "p2p":
        print_row("Usable Hosts",    f"{usable} (RFC 3021 — both IPs usable)", 'green')
        print_row("Host A",          first_host,                   'green')
        print_row("Host B",          last_host,                    'green')
    elif special == "single":
        print_row("Usable Hosts",    "1 (single host /32)",        'green')
        print_row("Host",            first_host,                   'green')
    else:
        print_row("Usable Hosts",    usable,                       'green')
        if first_host:
            print_row("First Host",  first_host,                   'green')
            print_row("Last Host",   last_host,                    'green')
        else:
            print_row("Hosts",       "None",                       'red')

    if not special and large_net:
        print()
        print(colored(f"  [!] Large network detected (>{SAFE_THRESHOLD} IPs) — host listing disabled to protect memory.", 'yellow', attrs=['bold']))
    elif not special and not large_net and list_hosts and first_host:
        print_section(f"All Usable Hosts  [{usable} total]")
        for ip in network.hosts():
            print(colored(f"    {ip}", 'white'))

    if save_file:
        print()
        print(colored(f"  [*] Writing hosts to {save_file} ...", 'cyan', attrs=['bold']))
        try:
            with open(save_file, "w") as f:
                if special == "p2p":
                    f.write(str(first_host) + "\n")
                    f.write(str(last_host)  + "\n")
                elif special == "single":
                    f.write(str(first_host) + "\n")
                else:
                    for ip in network.hosts():
                        f.write(str(ip) + "\n")
            print(colored(f"  [+] Host list saved → {save_file}", 'green', attrs=['bold']))
        except PermissionError:
            print(colored(f"  [!] Permission denied — cannot write to '{save_file}'", 'red', attrs=['bold']))
            print(colored( "  [?] Try: sudo python3 cidr_range.py  or  save to ~/Desktop/", 'yellow'))
        except FileNotFoundError:
            print(colored(f"  [!] Directory not found — '{save_file}'", 'red', attrs=['bold']))
            print(colored( "  [?] Make sure the folder exists before saving.", 'yellow'))
        except IsADirectoryError:
            print(colored(f"  [!] '{save_file}' is a directory, not a file.", 'red', attrs=['bold']))
            print(colored( "  [?] Try a filename like: hosts.txt or /tmp/hosts.txt", 'yellow'))
        except OSError as e:
            print(colored(f"  [!] File write failed — {e}", 'red', attrs=['bold']))
            print(colored( "  [?] Check disk space or path validity.", 'yellow'))

    print()
    print(colored("  ──────────────────────────────────────────────────────────────", 'cyan'))
    print(colored("  [+] Done! ⚡", 'green', attrs=['bold']))
    print(colored("  ──────────────────────────────────────────────────────────────\n", 'cyan'))
    return True

def main():
    print_banner()

    print(colored("  [~] Initializing...", 'cyan', attrs=['bold']))
    time.sleep(0.4)
    print(colored("  [~] Loading modules...", 'cyan', attrs=['bold']))
    time.sleep(0.3)
    print(colored("  [+] Ready!\n", 'green', attrs=['bold']))
    time.sleep(0.2)

    while True:
        cidr, list_hosts, save_file = get_input()
        analyze_cidr(cidr, list_hosts=list_hosts, save_file=save_file)

        print(colored("  ┌──────────────────────────────────────────────────────────────", 'cyan'))
        again = ask_yn("  │  [?] Analyze another CIDR? (y/n)       : ")
        print(colored("  └──────────────────────────────────────────────────────────────\n", 'cyan'))

        if again != 'y':
            print(colored("  [+] Exiting CIDR Tool! ⚡\n", 'green', attrs=['bold']))
            sys.exit(0)

        clear()
        print_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n\n  [!] Interrupted by user. Exiting...\n", 'yellow', attrs=['bold']))
        sys.exit(0)