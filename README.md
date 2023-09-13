# Python CPU bound tasks - Performance Benchmark

This project aims to benchmark the performance of different Python concurrency approaches for four types of workloads:
sequential, thread pool with 100 workers, thread pool with 10 workers, and using multiprocessing pool. The focus is on
measuring the 90th percentile (p90) performance for each approach while executing with varying data input sizes.

## Motivation

Understanding the performance characteristics of different concurrency strategies is crucial for developing efficient
and scalable Python applications. This benchmark project provides insights into how various multiprocessing techniques
perform under different workloads and input sizes. Also, it's important to prove that threads for CPU bounded tasks that do not work well in Python because of GIL.

## Workloads

1. **Sequential**: This approach represents the baseline performance of executing tasks sequentially.
2. **Thread Pool (100 workers)**: This approach utilizes a thread pool with 100 workers to parallelize tasks.
3. **Thread Pool (10 workers)**: This approach utilizes a thread pool with 10 workers to parallelize tasks.
4. **Multiprocessing Pool**: This approach utilizes the `multiprocessing` module to distribute tasks among multiple
   processes.

## Results

![Benchmark Image](python_cpu_bound_tasks.png) <!-- Replace with the actual path to your benchmark image -->

## Usage

1. Ensure you have **Python 3.10** installed. You can download it from
   the [official Python website](https://www.python.org/downloads/release).

2. Clone this repository:
   ```sh
   git clone git@github.com:luisgsilva950/research-python-concurrency-benchmark.git
   cd research-python-concurrency-benchmark
   virtualenv venv 
   source venv/bin/activate
   pip install -r requirements.txt
   python3 benchmark.py
