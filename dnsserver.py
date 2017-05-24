import socket
import sys, os
from multiprocessing import Process
import signal


class DNS(Process):
    nth = {
        0: "second",
        1: "third",
    }

    def __init__(self, name, port, file, dnsServices):
        super(DNS, self).__init__()
        self.name = name
        self.port = port
        self.file = file
        self.dnsServices = dnsServices
        self.answer = {}
        lines = file.readlines()
        ans = {line.split(' ')[0]: line.split(' ')[1] for line in lines}
        for line in lines:
            parts = line.split(" ")
            self.answer[parts[0]] = parts[1]

    def query(self, addr, host):
        for i in self.answer:
            if addr == i:
                return self.answer[i]
        if len(self.dnsServices) == 0:
            return 'no results'
        for dns in self.dnsServices:
            print("%s(%s) is trying to connect to the %s DNS, port %s" % (self.name,
                                                                          os.getpid(),
                                                                          self.nth[self.dnsServices.index(dns)],
                                                                          dns.port))
            sock = socket.socket()
            sock.connect(('localhost', dns.port))
            print("success connect")
            print("%s(%s) sending origin data: %s" % (self.name, os.getpid(),
                                                      host.decode("utf-8")))
            sock.send(host)
            data = sock.recv(1024)
            print("%s(%s) received from %s DNS: %s" % (self.name,
                                                       os.getpid(), self.nth[self.dnsServices.index(dns)], data))
            sock.close()
            if data.decode("utf-8") != "no results":
                return data.decode("utf-8")

        self.conn.send(self.answer)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', self.port))
        sock.listen(1)
        try:
            self.conn, self.addr = sock.accept()
            # while True:
            self.conn.settimeout(60)
            data = self.conn.recv(1024)
            edata = data.decode("utf-8")
            res = self.query(edata, data)
            print("%s(%s) found the res: %s" % (self.name,
                                                os.getpid(), res))
            self.conn.send(res.encode('utf-8'))
        finally:
            self.conn.close()


if __name__ == '__main__':
    f1 = open('addresses.url')
    f2 = open('alternative_addresses.url')
    f3 = open('alternative_addresses2.url')
    dns2 = DNS('DNS2', 9091, f2, [])
    dns3 = DNS('DNS3', 9092, f3, [])
    dns1 = DNS('DNS1', 9090, f1, [dns2, dns3])
    print('main PID:', os.getpid())
    dns1.start()
    dns2.start()
    dns3.start()
