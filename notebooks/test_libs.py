import time

def sleep(timeout = 1.0):
    target = time.time() + timeout
    now = time.time()
    while now < target:
        now = time.time()
