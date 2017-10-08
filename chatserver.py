import select
import socket
import sys


HOST = ''
PORT = 2048
CLIENTS = []


def broadcast(server, omitted_client, message):
    for client in CLIENTS:
        if client != server and client != omitted_client:
            try:
                client.send(message)
            except socket.error:
                client.close()
                if client in CLIENTS:
                    CLIENTS.remove(client)


def chat_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)

    CLIENTS.append(server)

    print 'Chat server started on port %d' % PORT

    while True:
        read_connections, _, _ = select.select(CLIENTS, [], [], 0)

        for client in read_connections:
            if client == server:
                new_client, address = server.accept()
                CLIENTS.append(new_client)
                print 'Client (%s, %s) connected' % address
                broadcast(server, new_client,
                          '[%s:%s] entered our chatting room\n' % address)
            else:
                try:
                    data = client.recv(4096)

                    if data:
                        broadcast(server, client,
                                  '\r[%s] %s' % (str(client.getpeername()), data))
                    else:
                        if client in CLIENTS:
                            CLIENTS.remove(client)
                        broadcast(server, client,
                                  'Client (%s, %s) is offline\n' % address)
                except socket.error:
                    broadcast(server, client,
                              'Client (%s, %s) is offline\n' % address)
                    continue

    server.close()


if __name__ == '__main__':
    sys.exit(chat_server())
