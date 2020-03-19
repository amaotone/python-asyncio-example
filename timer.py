import time
from contextlib import contextmanager


@contextmanager
def timer(name):
    t0 = time.time()
    print("=" * 50)
    print(f"[{name}] start")
    yield
    print(f"[{name}] done in {time.time() - t0:.1f} s")
    print("=" * 50)

