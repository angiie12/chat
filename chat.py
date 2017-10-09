import socket
import sys
import threading
import time


CLIENTS = {}


def add_client(host, address):
    try:
        client_address = (host, address)

        client = socket.socket()
        client.connect(client_address)

        CLIENTS[client_address] = client

        print 'Connected with %s:%d.' % client_address

        threading.Thread(target=handle_conversation,
                         args=(client, client_address,)).start()
    except socket.error:
        print 'Could not connect with %s:%d.' % client_address


def chat_server(port):
    server_address = ('', port)

    server = socket.socket()
    server.bind(server_address)
    server.listen(10)

    print 'Chat server is listening on localhost, port %d.' % port

    while True:
        client, address = server.accept()
        CLIENTS[address] = client 

        sys.stdout.write('Client %s:%s joined.\n>>> ' % address)
        sys.stdout.flush()

        threading.Thread(target=handle_conversation,
                         args=(client, address,)).start()

    server.close()


def handle_conversation(client, address):
    while True:
        try:
            data = client.recv(1024)

            if not data:
                break

            sys.stdout.write('\n[%s:%s] %s\n>>> ' % (address[0], address[1], data))
            sys.stdout.flush()

        except socket.error:
            break

    # remove_client(client, address)

    client.close()

    sys.stdout.write('\nClient %s:%s disconnected.\n>>> ' % address)
    sys.stdout.flush()


def list_connected_clients():
    print '%4s\t%11s\t%s' % ('id:', 'IP Address', 'Port')

    for count, address in enumerate(CLIENTS):
        print '%4d\t%11s\t%d' % (count, address[0], address[1])


# def remove_client(client, address):
#     pass


def main():
    # TODO To terminate the chat_server, it would be better to make it a class.
    threading.Thread(target=chat_server, args=(2048,)).start()
    time.sleep(0.1)

    while True:
        response = raw_input('>>> ')

        if response.lower().startswith('connect'):
            response = response.split(' ')
            add_client(response[1], int(response[2]))
        elif ':quit' in response:
            pass
        elif response.lower().startswith('list'):
            list_connected_clients()
        else:
            for address in CLIENTS:
                CLIENTS[address].send(response)


if __name__ == '__main__':
    main()
