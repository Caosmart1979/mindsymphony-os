#!/usr/bin/env python3
"""
Start one or more servers, wait for them to be ready, run a command, then clean up.

Usage:
    # Single server
    python scripts/with_server.py --server "npm run dev" --port 5173 -- python automation.py
    python scripts/with_server.py --server "npm start" --port 3000 -- python test.py

    # Multiple servers
    python scripts/with_server.py \
      --server "cd backend && python server.py" --port 3000 \
      --server "cd frontend && npm run dev" --port 5173 \
      -- python test.py

SECURITY WARNING:
    This script uses shell=True for subprocess execution to support commands with
    cd and &&. Only use with TRUSTED input. Never pass untrusted user input to
    --server arguments as it could lead to command injection vulnerabilities.

    For production use, consider using --cwd option with shell=False instead.
"""

import subprocess
import socket
import time
import sys
import argparse
import shlex
import os
import re
from pathlib import Path

def is_server_ready(port, timeout=30):
    """Wait for server to be ready by polling the port."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def validate_server_command(cmd: str) -> None:
    """
    Validate server command for obvious security issues.

    Raises:
        ValueError: If command contains suspicious patterns
    """
    # Dangerous patterns that should not be in server commands
    dangerous_patterns = [
        r'rm\s+-rf',  # Destructive file operations
        r';\s*rm',    # Command chaining with rm
        r'\|\s*sh',   # Piping to shell
        r'`.*`',      # Command substitution
        r'\$\(',      # Command substitution
        r'>\s*/dev/', # Device file access
        r'curl.*\|',  # Download and execute
        r'wget.*\|',  # Download and execute
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, cmd, re.IGNORECASE):
            raise ValueError(
                f"Command contains potentially dangerous pattern: {pattern}\n"
                f"Command: {cmd}\n"
                f"This script only accepts server start commands."
            )


def parse_server_command(cmd: str):
    """
    Parse server command to extract working directory and command parts.

    Returns:
        tuple: (cwd, command_list) or (None, cmd) if complex shell needed
    """
    # Try to parse "cd dir && command" pattern
    cd_pattern = r'^cd\s+([^\s&]+)\s+&&\s+(.+)$'
    match = re.match(cd_pattern, cmd.strip())

    if match:
        cwd = match.group(1)
        command = match.group(2)

        # Validate directory path
        if '..' in cwd or cwd.startswith('/'):
            raise ValueError(f"Invalid directory path: {cwd}")

        # Try to parse the command safely
        try:
            cmd_parts = shlex.split(command)
            return (cwd, cmd_parts)
        except ValueError:
            # Complex command, fall back to shell
            return (None, cmd)

    # Simple command without cd
    try:
        cmd_parts = shlex.split(cmd)
        return (None, cmd_parts)
    except ValueError:
        # Complex shell command
        return (None, cmd)


def main():
    parser = argparse.ArgumentParser(
        description='Run command with one or more servers',
        epilog='WARNING: Only use with trusted input. See docstring for security notes.'
    )
    parser.add_argument('--server', action='append', dest='servers', required=True,
                       help='Server command (can be repeated)')
    parser.add_argument('--port', action='append', dest='ports', type=int, required=True,
                       help='Port for each server (must match --server count)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Timeout in seconds per server (default: 30)')
    parser.add_argument('--no-validation', action='store_true',
                       help='Skip security validation (use with extreme caution)')
    parser.add_argument('command', nargs=argparse.REMAINDER,
                       help='Command to run after server(s) ready')

    args = parser.parse_args()

    # Remove the '--' separator if present
    if args.command and args.command[0] == '--':
        args.command = args.command[1:]

    if not args.command:
        print("Error: No command specified to run")
        sys.exit(1)

    # Parse server configurations
    if len(args.servers) != len(args.ports):
        print("Error: Number of --server and --port arguments must match")
        sys.exit(1)

    servers = []
    for cmd, port in zip(args.servers, args.ports):
        # Validate command for security issues
        if not args.no_validation:
            try:
                validate_server_command(cmd)
            except ValueError as e:
                print(f"Error: Security validation failed for command: {cmd}")
                print(f"Reason: {e}")
                print("\nIf you're sure this command is safe, use --no-validation flag")
                sys.exit(1)

        # Parse command to use safer execution when possible
        cwd, parsed_cmd = parse_server_command(cmd)

        servers.append({
            'cmd': cmd,
            'parsed_cmd': parsed_cmd,
            'cwd': cwd,
            'port': port
        })

    server_processes = []

    try:
        # Start all servers
        for i, server in enumerate(servers):
            print(f"Starting server {i+1}/{len(servers)}: {server['cmd']}")

            # Try to use safer execution method
            if isinstance(server['parsed_cmd'], list):
                # Can use shell=False with parsed command
                print(f"  → Using safe execution (shell=False)")
                process = subprocess.Popen(
                    server['parsed_cmd'],
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=server['cwd']
                )
            else:
                # Complex command requires shell
                print(f"  ⚠️  Using shell execution (security risk with untrusted input)")
                if not args.no_validation:
                    print(f"  ✓  Command passed security validation")
                process = subprocess.Popen(
                    server['cmd'],
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

            server_processes.append(process)

            # Wait for this server to be ready
            print(f"Waiting for server on port {server['port']}...")
            if not is_server_ready(server['port'], timeout=args.timeout):
                raise RuntimeError(f"Server failed to start on port {server['port']} within {args.timeout}s")

            print(f"Server ready on port {server['port']}")

        print(f"\nAll {len(servers)} server(s) ready")

        # Run the command
        print(f"Running: {' '.join(args.command)}\n")
        result = subprocess.run(args.command)
        sys.exit(result.returncode)

    finally:
        # Clean up all servers
        print(f"\nStopping {len(server_processes)} server(s)...")
        for i, process in enumerate(server_processes):
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            print(f"Server {i+1} stopped")
        print("All servers stopped")


if __name__ == '__main__':
    main()