import socket, sys


class Client():
    def run(self, host):
        sock = socket.socket()
        sock.connect(('localhost', 9090))
        # print("client: ", host)
        print("clientb: ", bytes(host))
        # print((host)).
        sock.send(bytes(host))
        data = sock.recv(1024)
        sock.close()
        print("Client recieved: ", data.decode("utf-8"))


c = Client()
host = "example3.com"
s = str(host).encode()
print(s)
c.run(s)
