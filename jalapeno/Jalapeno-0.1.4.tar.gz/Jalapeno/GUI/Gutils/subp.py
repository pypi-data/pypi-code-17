import subprocess 
import sys
from multiprocessing import Process
import time
def testing():
	test = subprocess.Popen([sys.executable,"Chrome.py"])
	print(test.pid)
	time.sleep(5)
	test.kill()

p = Process(target = testing)
p.start()
print(p)
time.sleep(1)
p.terminate()