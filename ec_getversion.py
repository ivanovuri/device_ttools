#! /usr/bin/env python3.8
# -*- coding: utf-8 -*-
import getpass
import argparse
import threading
from helpers import edgecore
from helpers import host
from helpers import auth


def GetCurrentVersion(ip, result):
    ver_output = edgecore.ExecuteReadViaTelnet(ip, 'show version')
    lines = ver_output.split('\n')

    for line in lines:
        if 'Operation Code Version' in line:
            result.append([ip,
                           line.split(':')[-1].lstrip().rstrip('\r')])
            return line.split(':')[-1].lstrip().rstrip('\r')

    return ''


def main():

    parser = argparse.ArgumentParser(description='Show active firmware version')

    parser.add_argument('switch_list',
                        type=str,
                        help='List of Edge-Core switches separated by space')

    parser.add_argument('-cf', '--credentials_file')

    args = parser.parse_args()

    edgecore.user, edgecore.password = auth.ReadCredentialsFromFile(args.credentials_file)
    
    switches = host.RemoveDuplicatesFromList(args.switch_list.split(' '))
    
    if not host.IsIpValid(switches):
        sys.exit('One or more IP addresses are not valid')

    up, down = host.SplitWorkingDeadHosts(switches)

    print('Hosts in Up state: %s' % ', '.join(up))
    print('Hosts in Down state: %s' % ', '.join(down))

    results = list()
    thread_list = list()

    for switch in up:
        thread_list.append(threading.Thread(target=GetCurrentVersion, args=(switch, results,)))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    line_num = 1
    for result in results:
        print('%2d. Ip: %s version: %s' % (line_num, result[0], result[1]))
        line_num +=1


if __name__ == '__main__':
    main()
