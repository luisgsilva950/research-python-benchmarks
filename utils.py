import time
from typing import List, Tuple

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


def plot(title: str, xs: Tuple[str, List[int]], values: List[Tuple[str, List[int]]]):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    x_legend, xs = xs
    colors = ('red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'brown', 'black')

    for idx, r in enumerate(values):
        legend, results = r
        plt.plot(xs, results, color=colors[idx % len(colors)], marker='o', label=legend)

    plt.xlabel(x_legend)
    plt.ylabel('seconds')
    plt.title(title)
    plt.legend()

    # plt.tight_layout()
    plt.savefig(f'figures/{title.replace(" ", "_").replace(".", "_").replace(":", "_")}'.lower(),
                facecolor='auto', edgecolor='auto', backend=None)

    plt.show()


def moving_average(data: List[int], window_size: int = 13):
    pad_size = (window_size - 1) // 2
    import numpy as np
    padded_data = np.pad(data, (pad_size, pad_size), mode='edge')
    smoothed_data = np.convolve(padded_data, np.ones(window_size) / window_size, mode='valid')
    return list(smoothed_data)
