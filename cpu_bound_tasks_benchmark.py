import gzip
import json
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from typing import List

from utils import timeit, plot


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


@timeit(executions=5)
def get_sequential_time(values: List[bytes]):
    sequential_results = []
    for value in values:
        sequential_results.append(gzip.decompress(value))
    return sequential_results


@timeit(executions=5)
def get_threadpool_100_workers_time(values: List[bytes]):
    executor = ThreadPoolExecutor(max_workers=100)
    futures = []
    for value in values:
        futures.append(executor.submit(gzip.decompress, data=value))
    futures = [f.result() for f in futures]
    return futures


@timeit(executions=5)
def get_threadpool_10_workers_time(values: List[bytes]):
    executor = ThreadPoolExecutor(max_workers=10)
    futures = []
    for value in values:
        futures.append(executor.submit(gzip.decompress, data=value))
    futures = [f.result() for f in futures]
    return futures


@timeit(executions=5)
def get_multiprocessing_pool_time(values: List[bytes]):
    with Pool(processes=4) as pool:
        return pool.map(gzip.decompress, values)


if __name__ == '__main__':
    xs = []
    seq_ys, threadpool_100_workers_ys, threadpool_10_workers_ys, multiprocessing_pool_ys = [], [], [], []
    for x in range(1, 100000, 100):
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

    plot(title="Comparison of CPU bound tasks using Python 3.10",
         xs=('nº tasks', xs),
         values=[('sequential', seq_ys),
                 ('threadpool 100 workers', threadpool_100_workers_ys),
                 ('threadpool 10 workers', threadpool_10_workers_ys),
                 ('multiprocessing pool', multiprocessing_pool_ys)])
