import select
import socket
import sys


def chat_client(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(2)

    try:
        client.connect(('', port))
    except socket.error:
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. You can start sending messages'
    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    while True:
        read_connections, _, _ = select.select([sys.stdin, client], [], [])

        for connection in read_connections:
            if connection == client:
                data = connection.recv(4096)

                if data:
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()
                else:
                    print '\nDisconnected from chat server'
                    sys.exit()
            else:
                message = sys.stdin.readline()
                client.send(message)
                sys.stdout.write('[Me] ')
                sys.stdout.flush()
