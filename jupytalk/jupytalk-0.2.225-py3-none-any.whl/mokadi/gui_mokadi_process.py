# -*- coding: utf-8 -*-
"""
@file
@brief Second process to listen to the mike. Issue: two processes
cannot listen to the mike at the same time.
"""

from multiprocessing import Process, Pipe


def process_listen(conn):
    from ensae_teaching_cs.pythonnet import vocal_recognition_listening
    for score, text in vocal_recognition_listening():
        conn.send(text)
    conn.close()


def start_process_listen():
    parent_conn, child_conn = Pipe()
    p = Process(target=process_listen, args=(child_conn,))
    p.start()
    return p, parent_conn, child_conn
