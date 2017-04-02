import threading
import queue

def debounce(iterable, delay):
  q = queue.Queue()
  def _enqueue_forever():
    for x in iterable:
      q.put(x)
  threading.Thread(target=_enqueue_forever, daemon=True).start()

  while True:
    buffer = [q.get()]
    while True:
      try:
        buffer.append(q.get(timeout=delay))
      except queue.Empty:
        break
    yield buffer
