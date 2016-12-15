from multiprocessing import Process, Pipe, Event
import time

k = 3


def p1(k1, e1, e2):
    i = 0

    print("  P1 started")
    for i in range(1,5):


        # print("  P1 has received a signal from P2")
        print("  P1 writes a message to K1")
        time.sleep(0.1)
        k1.send({'id': 2, 'text': "this is id of P2"[:30]})
        time.sleep(0.1)
        print("  P1 is waiting for a signal from P0")
        e1.wait()
        time.sleep(0.1)

        ##############333
        print("  P1 sends a signal to P2")
        time.sleep(0.1)
        e2.set()
    #
    # print("  P1 writes a message to K1")
    # time.sleep(0.1)
    # k1.send({'id': 1, 'text': "Hello from P1 again"[:30]})
    # time.sleep(0.1)

    #############3
    print("  P1 finished")


def p2(k1, e1, e2):
    print("  P2 started")
    time.sleep(0.1)
    for i in range(1,5):

        print("  P2 writes a message to K1")
        time.sleep(0.1)
        k1.send({'id': 2, 'text': "Hello from P2"[:30]})
        time.sleep(0.1)

        # print("  P2 sends a signal to P1")
        # time.sleep(0.1)
        #
        # e1.set()
        ##########33

        print("  P2 is waiting for a signal from P1")
        e2.wait()
        time.sleep(0.1)

        print("  P2 has received a signal from P1")

    #
        #
        # print ("  P2 writes a message to K1")
        # time.sleep(0.1)
        #
        # print ("  P2 sends a signal to P1")
        # time.sleep(0.1)
        # e1.set()
    #############33
    print("  P2 finished")


if __name__ == "__main__":
    print("P0 started")

    k1, k1_2 = Pipe()
    k2, k2_2 = Pipe()

    e1 = Event()
    e2 = Event()

    pp1 = Process(target=p1, args=(k1, e1, e2,))
    pp2 = Process(target=p2, args=(k1, e1, e2,))

    pp2.start()

    pp1.start()

    messages = 8
    while messages > 0:
        mess = k1_2.recv()
        print("P0 has read the message from K1: " + str(mess))
        messages -= 1

        print("  P0 sends a signal to P1")
        time.sleep(0.1)

        e1.set()
    pp2.join()
    pp1.join()

    print("P0 finished")