import subprocess

class RestartableProcess:
  def __init__(self, *popen_args, **popen_kwargs):
    self.popen_args = popen_args
    self.popen_kwargs = popen_kwargs
    self.process = None

  def start(self):
    self.process = subprocess.Popen(*self.popen_args, **self.popen_kwargs)
  def stop(self, timeout=None):
    if self.process is not None:
      self.process.kill()
      self.process.wait(timeout)
      self.process.kill()
  def restart(self):
    self.stop()
    self.start()

  def __enter__(self):
    self.start()
    return self
  def __exit__(self, exc_type, exc_value, traceback):
    pass
