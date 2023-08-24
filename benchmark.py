import gzip
import json
import time

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from typing import List
from numpy import percentile


def timeit(executions: int = 1):
    def function_wrapper(function):
        def wrapper(*function_args, **function_kwargs):
            execution_times = []
            for _ in range(executions):
                st = time.time()
                function(*function_args, **function_kwargs)
                execution_times.append(round(time.time() - st, 4))
            execution_times.sort()
            return percentile(execution_times, 90)

        wrapper.__name__ = function.__name__
        return wrapper

    return function_wrapper


def generate_x_gzipped_values(size: int):
    import io
    import gzip
    values = []
    for i in range(size):
        dummy_data = f"This is dummy data {i + 1}"
        buffer_ = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer_, mode='wb') as f:
            f.write(dummy_data.encode('utf-8'))
        values.append(buffer_.getvalue())
    return values


@timeit(executions=10)
def get_sequential_time(values: List[bytes]):
    sequential_results = []
    for value in values:
        sequential_results.append(gzip.decompress(value))
    return sequential_results


@timeit(executions=10)
def get_threadpool_100_workers_time(values: List[bytes]):
    executor = ThreadPoolExecutor(max_workers=100)
    futures = []
    for value in values:
        futures.append(executor.submit(gzip.decompress, data=value))
    futures = [f.result() for f in futures]
    return futures


@timeit(executions=10)
def get_threadpool_10_workers_time(values: List[bytes]):
    executor = ThreadPoolExecutor(max_workers=10)
    futures = []
    for value in values:
        futures.append(executor.submit(gzip.decompress, data=value))
    futures = [f.result() for f in futures]
    return futures


@timeit(executions=10)
def get_multiprocessing_pool_time(values: List[bytes]):
    with Pool() as pool:
        return pool.map(gzip.decompress, values)


if __name__ == '__main__':
    xs = []
    seq_ys, threadpool_100_workers_ys, threadpool_10_workers_ys, multiprocessing_pool_ys = [], [], [], []
    for x in [10, 500, 5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]:
        xs.append(x)
        compressed_values = generate_x_gzipped_values(size=x)
        seq_ys.append(get_sequential_time(values=compressed_values))
        print(get_sequential_time.__name__, x, seq_ys[-1])
        threadpool_100_workers_ys.append(get_threadpool_100_workers_time(values=compressed_values))
        print(get_threadpool_100_workers_time.__name__, x, threadpool_100_workers_ys[-1])
        threadpool_10_workers_ys.append(get_threadpool_10_workers_time(values=compressed_values))
        print(get_threadpool_10_workers_time.__name__, x, threadpool_10_workers_ys[-1])
        multiprocessing_pool_ys.append(get_multiprocessing_pool_time(values=compressed_values))
        print(get_multiprocessing_pool_time.__name__, x, multiprocessing_pool_ys[-1])

    results = {"xs": xs,
               "seq_ys": seq_ys,
               "threadpool_100_workers_ys": threadpool_100_workers_ys,
               "threadpool_10_workers_ys": threadpool_10_workers_ys,
               "multiprocessing_pool_ys": multiprocessing_pool_ys}

    with open("python_decompress_seq_thread_multiprocessing.json", "w") as fp:
        json.dump(results, fp=fp)

    import matplotlib.pyplot as plt

    plt.plot(results["xs"], results["seq_ys"], color='maroon', marker='o', label="sequential")
    plt.plot(results["xs"], results["threadpool_100_workers_ys"], color='blue', marker='o', label="threadpool 100 workers")
    plt.plot(results["xs"], results["threadpool_10_workers_ys"], color='green', marker='o', label="threadpool 10 workers")
    plt.plot(results["xs"], results["multiprocessing_pool_ys"], color='red', marker='o', label="multiprocessing pool")
    plt.xlabel('nº tasks')
    plt.ylabel('seconds')
    plt.title("Comparison of CPU bound tasks using Python 3.10")
    plt.legend()
    plt.show()
