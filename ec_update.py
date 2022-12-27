#! /usr/bin/env python3.8
# -*- coding: utf-8 -*-
import getpass
import argparse
import threading
from os.path import join as path_join
from helpers import edgecore
from helpers import host
from helpers import auth

def main():
    update_cmd = '''
copy tftp file\r
%s\r
2\r
%s\r
%s\r
configure\r
 boot system opcode:%s\r
 exit\r
reload\r
y\r
    '''

    parser = argparse.ArgumentParser(description='Update firmware')

    parser.add_argument('switch_list',
                        type=str,
                        help='List of Edge-Core switches separated by space')
    parser.add_argument('tftp_server',
                        type=str,
                        help='TFTP server where firmwares are stored')
    parser.add_argument('tftp_dir',
                        type=str,
                        help='TFTP server firmware path')
    parser.add_argument('firmware_name',
                        type=str,
                        help='New firmware to download from tftp')
    parser.add_argument('-cf', '--credentials_file')

    args = parser.parse_args()

    edgecore.user, edgecore.password = auth.ReadCredentialsFromFile(args.credentials_file)

    switches = host.RemoveDuplicatesFromList(args.switch_list.split(' '))
    
    if not host.IsIpValid(switches):
        sys.exit('One or more IP addresses are not valid')

    up, down = host.SplitWorkingDeadHosts(switches)

    print('Hosts in Up state: %s' % ', '.join(up))
    print('Hosts in Down state: %s' % ', '.join(down))

    for switch in up:
        inactive_fw = ''

        try:
            inactive_fw = edgecore.InactiveFirmware(switch)
        except FileNotFoundError:
            print('No unused firmwares on device %s.' % switch)
            continue

        edgecore.ExecuteReadViaTelnet(switch, 'delete file name %s' % inactive_fw)

    commands = update_cmd % (args.tftp_server,
                             path_join(args.tftp_dir, args.firmware_name),
                             args.firmware_name,
                             args.firmware_name)

    thread_list = list()
    for switch in up:
        # thread_list.append(threading.Thread(target=edgecore.ExecuteReadViaTelnet, args=(switch, commands,)))
        thread_list.append(threading.Thread(target=edgecore.ExecuteViaTelnet, args=(switch, commands,)))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print('End reached...')


if __name__ == '__main__':
    main()
