import multiprocessing

class Worker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # None values means shutdown
                print '%s: Exiting' % self.name
                self.task_queue.task_done()
                break
            result = next_task()
            self.task_queue.task_done()
            self.result_queue.put(result)
        return

class IteratorWorker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # None values means shutdown
                print '%s: Exiting' % self.name
                self.task_queue.task_done()
                break
            result_iterator = next_task()
            for result in result_iterator:
                self.result_queue.put(result)
            self.task_queue.task_done()
        return
