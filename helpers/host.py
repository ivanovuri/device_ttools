#! /usr/bin/env python3.8
# -*- coding: utf-8 -*-
import socket


def IsIpValid(switches):
    valid = True

    for switch in switches:
        try:
            socket.inet_aton(switch)
        except socket.error:
            valid = False
            break

    return valid


def SplitWorkingDeadHosts(switches):
    working_hosts = list()
    dead_hosts = list()

    for switch in switches:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_STREAM)

        location = (switch, 23)

        result = sock.connect_ex(location)
        if result == 0:
            working_hosts.append(switch)
        else:
            dead_hosts.append(switch)

        sock.close()

    return working_hosts, dead_hosts


def RemoveDuplicatesFromList(switches):
     return list(dict.fromkeys(switches))
