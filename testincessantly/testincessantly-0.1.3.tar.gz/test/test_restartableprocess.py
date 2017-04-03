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

def test_stop():
  p = testincessantly.RestartableProcess(['sleep', 'infinity'])
  p.start()
  p.stop()

def test_stop_respects_timeout():
  p = testincessantly.RestartableProcess('trap "true" TERM; echo "I am invincible!"; sleep infinity', shell=True, stdout=subprocess.PIPE)
  p.start()
  p.process.stdout.readline()
  p.stop(timeout=0.01)
  assert p.process.returncode == -9

def test_context_management():
  with testincessantly.RestartableProcess(['echo', 'hi'], stdout=subprocess.PIPE) as p:
    p.process.wait()
  assert p.process.returncode == 0
