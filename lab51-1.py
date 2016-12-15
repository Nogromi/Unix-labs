from multiprocessing import Process, Pipe, Event
import time


def p1(k1, k2, k2_son, e1, e2, e3):
    print("- P1 started")
    pp2 = Process(target=p2, args=(k1, k2, e1, e2, e3,))
    pp2.start()
    time.sleep(0.1)
    k1.send(message)
    print("- P1 sent id of P2 via K1: " + str(message))
    time.sleep(0.1)

    print("- P1 is waiting for signal #1 from P0")
    e1.wait()
    time.sleep(0.1)

    print("- P1 has received signal #1 from P0")
    time.sleep(0.1)


    message = k2_son.recv()
    print("- P1 received a message via K2: " + str(message))
    time.sleep(0.1)
    k1.send(message)
    print("- P1 sent a message via K1: " + str(message))
    time.sleep(0.1)
    k1.send(pp2.pid)
    print("- P1 sent P2 id via K1")

    time.sleep(0.1)
    pp2.join()
    print("- P1 finished")


def p2(k1, k2, e1, e2, e3):
    print("-- P2 started")
    time.sleep(0.1)

    print("-- P2 is waiting for signal #2 from P0")
    e2.wait()
    time.sleep(0.1)
    print("-- P2 received a signal #2 from P1")
    time.sleep(0.1)
    message = "Message from P2: hey, kids!"
    k2.send(message)
    print("-- P2 sent a message via K2: " + message)
    time.sleep(0.1)

    print("-- P2 is waiting for signal #3 from P0")
    e3.wait()
    time.sleep(0.1)
    print("-- P2 received a signal #3 from P0")
    time.sleep(0.1)

    message = "Message from P2: hey there again!"
    k1.send(message)
    time.sleep(0.1)
    print("-- P2 sent a message via K1: " + message)

    time.sleep(0.1)
    print("-- P2 finished")


if __name__ == "__main__":
    print("P0 started")

    k1, k1_son = Pipe()
    k2, k2_son = Pipe()
    e1 = Event()
    e2 = Event()
    e3 = Event()

    pp1 = Process(target=p1, args=(k1, k2, k2_son, e1, e2, e3,))
    time.sleep(0.1)
    pp1.start()
    time.sleep(0.1)
    print("- P0 is sending a signal #2 to P2")
    time.sleep(0.1)
    e2.set()

    print("P0 is sending a signal #1 to P1")
    e1.set()

    message = k1_son.recv()
    time.sleep(0.1)
    print("P0 received a message via K1: " + str(message))

    message = k1_son.recv()
    time.sleep(0.1)
    print("P0 received id of P2 via K1")
    pp2 = message

    print("P0 is sending a signal #3 to P2")
    e3.set()
    time.sleep(0.1)

    message1 = k1_son.recv()
    time.sleep(0.1)
    print("P0 received a message via K1: " + str(message1))

    pp1.join()
    print("P0 finished")
