#! /usr/bin/env python3.8
# -*- coding: utf-8 -*-
from telnetlib import Telnet

user = ''
password = ''

def ExecuteViaTelnet(ip, command):

    with Telnet(ip, 23) as tn:

        tn.read_until(b'Username: ')
        tn.write(user.encode('ascii') + b'\n')

        tn.read_until(b'Password: ')
        tn.write(password.encode('ascii') + b'\n')

        tn.read_until(b'#')
        tn.write(command.encode('ascii') + b'\n')

        tn.write(b"exit\n")


def ExecuteReadViaTelnet(ip, command):
    with Telnet(ip, 23) as tn:

        tn.read_until(b'Username: ')
        tn.write(user.encode('ascii') + b'\n')

        tn.read_until(b'Password: ')
        tn.write(password.encode('ascii') + b'\n')

        tn.read_until(b'#')
        tn.write(command.encode('ascii') + b'\n')

        tn.write(b"exit\n")

        result = tn.read_all().decode('ascii')

    return result


def InactiveFirmware(ip):
    dir_output = ExecuteReadViaTelnet(ip, 'dir')

    lines = dir_output.split('\n')
    
    firmwares = list()

    for line in lines:
        if 'OpCode' in line:
            firmwares.append(list(filter(None, line.split(' '))))
    
    for firmware in firmwares:
        if firmware[2] == 'N':
            return firmware[0]

    raise FileNotFoundError('Inactive firmware doesn\'t exists on device %s' % ip)
    