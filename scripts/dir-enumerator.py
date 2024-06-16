import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
import sys


def handle(*, url, path, extensions, status_blacklist):

    for ext in extensions:
        _path = f'/{path}'
        if ext:
            _path += f'.{ext}'

        response = requests.get(
            url=f'{url}/{_path}',
            headers={'Connection': 'close'}
        )

        if response.status_code in status_blacklist:
            print('.', end='', flush=True, file=sys.stderr)
        else:
            print('\n[+]', response.status_code, ':', _path)


def enumerate(
    *, url, wordlist, extensions, status_blacklist, thread_count
):

    executor = ThreadPoolExecutor(max_workers=thread_count)
    with open(wordlist, encoding='ISO-8859-15') as f:
        line = f.readline()
        while line:
            path = line.strip()
            executor.submit(
                handle,
                url=url,
                path=path,
                extensions=extensions,
                status_blacklist=status_blacklist
            )
            line = f.readline()
    executor.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Enumerator')
    parser.add_argument(
        '--url',
        type=str, required=True, help='URL to process'
    )
    parser.add_argument(
        '-w', '--wordlist',
        type=str, required=True, help='wordlist to process'
    )
    parser.add_argument(
        '-e', '--extensions',
        type=str, default=[''], help='extensions to process', action='append'
    )
    parser.add_argument(
        '-s', '--status-blacklist',
        type=int, default=[404], help='status codes to ignore', action='append'
    )
    parser.add_argument(
        '-t', '--thread-count',
        default=3, type=int, help='number of threads'
    )
    args = parser.parse_args()
    enumerate(**args.__dict__)
