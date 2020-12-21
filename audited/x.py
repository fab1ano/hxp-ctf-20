#!/usr/bin/env python
"""audited exploit."""
import sys
from pathlib import Path

from pwn import *

context.log_level = 'info'

BINARY = './files/audited.py'
HOST = '157.90.27.234'
PORT = 8007

MY_CODE = Path('./content.py').read_bytes()


def exploit(p, mode, payload=None):
    """Just pastes the content of content.py."""
    payload = payload or MY_CODE

    p.recvuntil('> ')
    p.sendline(payload)
    p.shutdown()

    print(p.recvall().decode('ascii'))


def main():
    """Does general setup and calls exploit."""
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <mode> [payload]')
        sys.exit(0)

    mode = sys.argv[1]

    if mode == 'exec':
        p = process(BINARY)
    elif mode == 'local':
        p = remote('localhost', PORT)
    elif mode == 'remote':
        p = remote(HOST, PORT)
    else:
        print('Invalid mode')
        sys.exit(1)

    if len(sys.argv) > 2:
        exploit(p, mode, payload=sys.argv[2])
    else:
        exploit(p, mode)

if __name__ == '__main__':

    main()
