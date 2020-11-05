#!/usr/bin/python3
import ipaddress
import re
import socket
import sys
from itertools import product

# TODO This is a quick and dirty implementation. Can be better.
# Should use a dictionary s.t {'ip': {'user': name, 'banner': banner, 'result': result}}

if len(sys.argv) != 3:
    print('Usage: vrfy.py <ip list> <user list>')
    sys.exit(0)

def vrfy(ip, user):

    # Create a Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the Server
    connect = s.connect((ip,25))

    # Receive the banner
    banner = s.recv(1024).decode('utf-8')

    # VRFY a user
    payload = ('VRFY ' + user + '\r\n').encode('utf-8')
    s.send(payload)
    result = s.recv(1024).decode('utf-8')

    # Close the socket
    s.close()

    # We only care about bingo's
    match = re.match(r'^252', result)

    bingo = False
    if match:
        bingo = True

    output = f'{ip}:\n\tbanner: {banner}\n\tresult: {result}'

    return user, output, bingo

def main():

    # TODO take cidr range
    # r = ipaddress.ip_network(sys.argv[1])
    with open(sys.argv[1]) as file:
        ipv4s = file.read().splitlines()

    with open(sys.argv[2]) as file:
        users = file.read().splitlines()

    ans = []
    # Get cartesian product of both lists
    for t in product(ipv4s,users):
        # Pass tuple to vrfy()
        ans.append((vrfy(t[0], t[1])))

    match = {}
    nomatch = {}
    for user, out, bingo in ans:
        if bingo:
            match.setdefault(user, []).append(out)
        else:
            nomatch.setdefault(user,[]).append(out)

    out = {'match': match, 'no match': nomatch}
    print(out)

if __name__ == '__main__':
    main()
