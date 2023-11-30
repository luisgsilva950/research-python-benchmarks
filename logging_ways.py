import json
import logging
from typing import List

from utils import timeit, plot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@timeit(executions=10)
def log_with_f_string(text: List[str]):
    logger.debug(f"Using f-string: {[2 * t[0] for t in text]}")


@timeit(executions=10)
def log_with_string_format(text: List[str]):
    logger.debug("Using string format: {}".format([2 * t[0] for t in text]))


@timeit(executions=10)
def log_with_logging_params(text: List[str]):
    logger.debug("Using logging parameters: %s", [2 * t[0] for t in text])


if __name__ == "__main__":
    xs = []
    f_string_ys, string_format_ys, logging_params_ys = [], [], []
    for size in range(1, 20000, 100):
        xs.append(size)
        texts = ["Hello, world!" for _ in range(size)]
        f_string_ys.append(log_with_f_string(texts))
        print(log_with_f_string.__name__, f_string_ys[-1])
        string_format_ys.append(log_with_string_format(texts))
        print(log_with_string_format.__name__, string_format_ys[-1])
        logging_params_ys.append(log_with_logging_params(texts))
        print(log_with_logging_params.__name__, logging_params_ys[-1])

    results = {"xs": xs,
               "f_string_ys": f_string_ys,
               "string_format_ys": string_format_ys,
               "logging_params_ys": logging_params_ys}

    with open("python_logging_ways.json", "w") as fp:
        json.dump(results, fp=fp)

    plot(title="Comparison of logging debug alternatives using Python 3.10 (LOG LEVEL: DEBUG)",
         xs=('nº of objects', xs),
         values=[('f string', f_string_ys),
                 ('string format', string_format_ys),
                 ('logging params', logging_params_ys)])
