import threading
import time
from typing import Callable

import schedule

from digestif.digest import create_digest


def run_threaded(job_func: Callable[..., None]):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


if __name__ == "__main__":
    create_digest()
    exit()
    schedule.every().day.at("06:30").do(run_threaded, create_digest)
    while 1:
        schedule.run_pending()
        time.sleep(1)
