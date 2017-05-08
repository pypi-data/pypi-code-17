from multiprocessing import Process, Pipe


def timeout(fun, time):
    recv_end, send_end = Pipe(False)
    p = Process(target=fun, args=(send_end,))
    p.start()
    p.join(time)
    if p.is_alive():
        p.terminate()
        print("Timeout, finishing earlier")

    r = []
    while recv_end.poll():
        r = recv_end.recv()
    return r
