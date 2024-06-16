import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
import re


def handle(*, url, subdomain):
    domain = re.sub('^http(s)?://', '', url)
    host = f'{subdomain}.{domain}'
    response = requests.get(
        url=url,
        headers={
            'Connection': 'close',
            'Host': host
        }
    )

    print(response.status_code, host)


def enumerate(*, url, wordlist, thread_count):

    executor = ThreadPoolExecutor(max_workers=thread_count)
    with open(wordlist, encoding='ISO-8859-15') as f:
        line = f.readline()
        while line:
            subdomain = line.strip()
            executor.submit(handle, url=url, subdomain=subdomain)
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
        '-t', '--thread-count',
        default=3, type=int, help='number of threads'
    )
    args = parser.parse_args()
    enumerate(**args.__dict__)
