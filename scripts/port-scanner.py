import argparse
import asyncio
import socket


async def check_port(*, host, port, timeout=1) -> tuple[int, bool]:
    try:
        loop = asyncio.get_event_loop()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            await loop.sock_connect(s, (host, port))
            print(f'[+] open: {port}')
            return port, True
    except:
        return port, False


async def scan_ports(*, host: str, ports: range, timeout: int = 1) -> list[tuple[int, bool]]:
    print(f'[+] scanning started {host}:[{ports.start}-{ports.stop}]')
    tasks = [check_port(host=host, port=port, timeout=timeout) for port in ports]
    return await asyncio.gather(*tasks)


def main(*, host, start_port, end_port, timeout):
    ports = range(start_port, end_port)
    results = asyncio.run(scan_ports(host=host, ports=ports, timeout=timeout))
    print(f'[+] {len(results)} hosts scanned')
    print(f'[+] {len([r for r in results if r[1]])} hosts found')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--host',
        required=True, help='the host to scan'
    )
    parser.add_argument(
        '-s', '--start-port',
        default=1, help='the lowest port to scan within the range (default: 1)'
    )
    parser.add_argument(
        '-e', '--end-port',
        default=65535, help='the highest port to scan within the range (default: 65535)'
    )
    parser.add_argument(
        '-t', '--timeout',
        default=1, help='the time to await the connection to etablish in seconds (default: 1s)'
    )
    main(**parser.parse_args().__dict__)

