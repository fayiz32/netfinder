#!/usr/bin/env python3
import argparse
import os
import socket
import sys

VERSION = "1.0.0"


def check_root():
    """1. Move root check up"""
    if hasattr(os, "geteuid") and os.geteuid() != 0:
        print("This program must be run as root.", file=sys.stderr)
        sys.exit(1)


def resolve_hostname(host):
    """4. Add socket.setdefaulttimeout(1) around hostname resolution"""
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(1)
    try:
        return socket.gethostbyname(host)
    except (socket.timeout, socket.gaierror) as exc:
        print(f"Could not resolve {host}: {exc}", file=sys.stderr)
        return None
    finally:
        socket.setdefaulttimeout(old_timeout)


def broadcast_srp(hosts):
    """2. Replace per-host srp with broadcast"""
    for host in hosts:
        ip = resolve_hostname(host)
        if ip is None:
            continue
        # TODO: replace this print with your actual broadcast SRP call
        print(f"Broadcasting SRP to {host} ({ip})")


def update_vendor(enabled):
    """5. Make vendor update opt-in"""
    if enabled:
        print("Updating vendor...")
        # TODO: call your vendor update routine here
    else:
        print("Skipping vendor update (use --update-vendor to enable)")


def main():
    parser = argparse.ArgumentParser(description="Example network tool")
    # 3. Add argparse --version
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    parser.add_argument(
        "--update-vendor",
        action="store_true",
        help="Enable vendor update (opt-in)",
    )
    parser.add_argument(
        "hosts",
        nargs="*",
        help="Hosts to broadcast to",
    )
    args = parser.parse_args()

    # 1. Move root check up (after parsing so --version works without root)
    check_root()

    # 2. Broadcast instead of per-host SRP
    broadcast_srp(args.hosts)

    # 5. Vendor update is now opt-in
    update_vendor(args.update_vendor)


if __name__ == "__main__":
    main()
