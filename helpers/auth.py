#! /usr/bin/env python3.8
# -*- coding: utf-8 -*-
import getpass


def ReadCredentialsFromFile(credentials_file):
    user = ''
    password = ''

    if credentials_file is None:
        user = input("Username: ")
        password = getpass.getpass('Password: ')
    else:
        credentials_file = open(credentials_file, 'r')
        credentials = credentials_file.readlines()
        if len(credentials) != 2:
            sys.exit('Incorrect credentials  file provided')
        else:
            user = credentials[0].lstrip().rstrip('\n')
            password = credentials[1].rstrip('\n')

    return user, password
