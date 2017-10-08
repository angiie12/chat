import select
import socket
import threading


class ChatServer(threading.Thread):

    def __init__(self, port):
        threading.Thread.__init__(self)

        self.clients = []
        self.port = port
        self.server = None

    def broadcast(self, omitted_client, message):
        for client in self.clients:
            if client != self.server and client != omitted_client:
                try:
                    client.send(message)
                except socket.error:
                    client.close()
                    if client in self.clients:
                        self.clients.remove(client)

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', self.port))
        self.server.listen(10)

        self.clients.append(self.server)

        print 'Chat server started on port %d' % self.port

        while True:
            read_connections, _, _ = select.select(self.clients, [], [], 0)

            for client in read_connections:
                if client == self.server:
                    new_client, address = self.server.accept()
                    self.clients.append(new_client)

                    print 'Client (%s, %s) connected' % address

                    self.broadcast(new_client, '[%s:%s] joined\n' % address)
                else:
                    try:
                        data = client.recv(4096)

                        if data:
                            self.broadcast(client, '\r[%s] %s' % (str(client.getpeername()), data))
                        else:
                            if client in self.clients:
                                self.clients.remove(client)
                            self.broadcast(client, 'Client (%s, %s) is offline\n' % address)
                    except socket.error:
                        self.broadcast(client, 'Client (%s, %s) is offline\n' % address)
                        continue

        self.server.close()
