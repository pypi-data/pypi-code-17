import subprocess
import testincessantly

def test_runs_when_started():
  p = testincessantly.RestartableProcess(['echo', 'hi'], stdout=subprocess.PIPE)
  p.start()
  p.process.wait()
  assert p.process.stdout.readline() == b'hi\n'

def test_runs_when_restarted():
  p = testincessantly.RestartableProcess(['echo', 'hi'], stdout=subprocess.PIPE)
  p.start()
  p.process.wait()
  assert p.process.stdout.readline() == b'hi\n'
  p.restart()
  p.process.wait()
  assert p.process.stdout.readline() == b'hi\n'

def test_context_management():
  with testincessantly.RestartableProcess(['echo', 'hi'], stdout=subprocess.PIPE) as p:
    p.process.wait()
  assert p.process.returncode == 0
