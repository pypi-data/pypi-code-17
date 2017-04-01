import sys
from multiprocessing import Pool

from cvbase.timer import Timer


class ProgressBar(object):
    """A progress bar which can print the progress"""

    def __init__(self, task_num=0, bar_width=50, start=True):
        self.task_num = task_num
        self.bar_width = 50
        self.completed = 0
        if start:
            self.start()

    def start(self):
        if self.task_num > 0:
            sys.stdout.write('[{}] 0/{}, elapsed: 0s, ETA:'.format(
                ' ' * self.bar_width, self.task_num))
        else:
            sys.stdout.write('completed: 0, elapsed: 0s')
        sys.stdout.flush()
        self.timer = Timer()

    def update(self):
        self.completed += 1
        elapsed = self.timer.since_start()
        fps = self.completed / elapsed
        if self.task_num > 0:
            percentage = self.completed / float(self.task_num)
            eta = int(elapsed * (1 - percentage) / percentage + 0.5)
            mark_width = int(self.bar_width * percentage)
            bar_chars = '>' * mark_width + ' ' * (self.bar_width - mark_width)
            sys.stdout.write(
                '\r[{}] {}/{}, {:.1f} task/s, elapsed: {}s, ETA: {:5}s'.format(
                    bar_chars, self.completed, self.task_num, fps,
                    int(elapsed + 0.5), eta))
        else:
            sys.stdout.write('completed: {}, elapsed: {}s, {:.1f} tasks/s'.
                             format(self.completed, int(elapsed + 0.5), fps))
        sys.stdout.flush()


def track_progress(func, tasks, bar_width=50, **kwargs):
    prog_bar = ProgressBar(len(tasks), bar_width)
    results = []
    for task in tasks:
        results.append(func(task, **kwargs))
        prog_bar.update()
    sys.stdout.write('\n')
    return results


def init_pool(process_num, initializer=None, initargs=None):
    if initializer is None:
        return Pool(process_num)
    elif initargs is None:
        return Pool(process_num, initializer)
    else:
        if not isinstance(initargs, tuple):
            raise TypeError('"initargs" must be a tuple')
        return Pool(process_num, initializer, initargs)


def track_parallel_progress(func,
                            tasks,
                            process_num,
                            initializer=None,
                            initargs=None,
                            bar_width=50,
                            chunksize=1,
                            skip_first=False,
                            keep_order=True):
    pool = init_pool(process_num, initializer, initargs)
    start = not skip_first
    task_num = len(tasks) - process_num * chunksize * int(skip_first)
    prog_bar = ProgressBar(task_num, bar_width, start)
    results = []
    if keep_order:
        gen = pool.imap(func, tasks, chunksize)
    else:
        gen = pool.imap_unordered(func, tasks, chunksize)
    for result in gen:
        results.append(result)
        if skip_first:
            if len(results) < process_num * chunksize:
                continue
            elif len(results) == process_num * chunksize:
                prog_bar.start()
                continue
        prog_bar.update()
    sys.stdout.write('\n')
    pool.close()
    pool.join()
    return results
