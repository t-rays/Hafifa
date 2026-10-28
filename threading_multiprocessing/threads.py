"""Run independent callables on a thread pool and keep submission order."""

import concurrent.futures
from logging import getLogger
from typing import Callable
from typing import TypeVar

logger = getLogger(__name__)


T = TypeVar("T")
# (callable, args, kwargs)
Job = tuple[Callable[..., T], tuple, dict]

def run_in_parallel(jobs: list[Job], max_workers: int) -> list[concurrent.futures.Future[T]]:
    """Submit each ``(func, args, kwargs)`` job and return futures in order.

    Every job has finished before this returns. An empty job list returns
    ``[]``. Exceptions stay on the futures; the caller reads them with
    ``Future.result``.
    """
    if not jobs:
        return []
    logger.info("Running %d jobs in thread pool (max_workers=%d)", len(jobs), max_workers)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(func, *args, **kwargs) for func, args, kwargs in jobs]
        concurrent.futures.wait(futures)
        return futures
