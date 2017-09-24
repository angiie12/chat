#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


def close_connection(*args):
    for arg in args:
        if len(arg) != 1:
            print('terminate <connection_id>')
            return

        # TODO Close connection here
        print('Client with ID: {} was closed!'.format(arg[0]))

        return

    print('terminate <connection_id>')


def connect(*args):
    for arg in args:
        if len(arg) != 2:
            print('connect <destination> <port>')
            return

        # TODO Do connections here

        return

    print('connect <destination> <port>')


def exit_client():
    sys.exit(0)


def get_help():
    with open('help', 'r') as help_prompt:
        for line in help_prompt:
            print(line.rstrip())


def get_ip_address():
    print('Local IPv6 Address: 0.0.0.0')
    print('External IPv6 Address: 0.0.0.0')


def list_connected_machines():
    print('ID\tIPv6 Address\tPort')


def send_message(*args):
    for arg in args:
        if len(arg) != 2:
            print('send <connection_id> <message>')
            return

        # TODO Send a message to specified host here

        return

    print('send <connection_id> <message>')


def main():
    if len(sys.argv) == 1:
        print('Usage: {} <port>'.format(sys.argv[0]))
        return

    try:
        port = int(sys.argv[1])
        if port <= 1024 or port > 66535:
            sys.stderr.write('{} is an invalid port number.\n'.format(port))
            return
    except ValueError:
        sys.stderr.write('"{}" is not a valid port number.\n'.format(sys.argv[1]))
        return

    options = {
        'connect': connect,
        'exit': exit_client,
        'help': get_help,
        'list': list_connected_machines,
        'myip': get_ip_address,
        'myport': port,
        'send': send_message,
        'terminate': close_connection
    }

    print('Peer-to-peer Chat Client 0.0.1')
    print('Type "help" for a list of available commands.')

    while True:
        params = input('>>> ').lower().split(' ')

        if params[0] == 'myport':
            print('Port: {}'.format(port))
        elif params[0] in options:
            if len(params) == 1:
                options[params[0]]()
            else:
                options[params[0]](params[1:])
        else:
            print('"{}" is not a valid command.'.format(params[0]))


if __name__ == '__main__':
    main()
