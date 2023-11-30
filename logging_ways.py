import json
import logging
from typing import List

from utils import timeit, plot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@timeit(executions=10)
def log_with_f_string(text: List[str]):
    logger.debug(f"Using f-string: {text}")


@timeit(executions=10)
def log_with_string_format(text: List[str]):
    # Arbitrary objects
    logger.debug("Using string format: {}".format(text))


@timeit(executions=10)
def log_using_percent_format(text: List[str]):
    logger.debug("Using percent format: %s" % (text))


@timeit(executions=10)
def log_with_logging_params(text: List[str]):
    logger.debug("Using logging parameters: %s", text)


@timeit(executions=10)
def log_checking_log_level(text: List[str]):
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Using logging parameters checking log level: %s", text)


if __name__ == "__main__":
    xs = []
    f_string_ys, string_format_ys, logging_params_ys, log_checking_log_level_ys, log_using_percent_ys = [], [], [], [], []
    for size in range(1, 20000, 100):
        xs.append(size)
        texts = ["Hello, world!" for _ in range(size)]
        f_string_ys.append(log_with_f_string(texts))
        print(log_with_f_string.__name__, f_string_ys[-1])
        string_format_ys.append(log_with_string_format(texts))
        print(log_with_string_format.__name__, string_format_ys[-1])
        logging_params_ys.append(log_with_logging_params(texts))
        print(log_with_logging_params.__name__, logging_params_ys[-1])
        log_checking_log_level_ys.append(log_checking_log_level(texts))
        print(log_checking_log_level.__name__, log_checking_log_level_ys[-1])
        log_using_percent_ys.append(log_using_percent_format(texts))
        print(log_using_percent_format.__name__, log_using_percent_ys[-1])

    results = {"xs": xs,
               "f_string_ys": f_string_ys,
               "string_format_ys": string_format_ys,
               "logging_params_ys": logging_params_ys,
               "logging_check_log_level_ys": log_checking_log_level_ys,
               "log_using_percent_ys": log_using_percent_ys}

    with open("results/python_logging_ways.json", "w") as fp:
        json.dump(results, fp=fp)

    plot(title="Comparison of logging debug alternatives using Python 3.10 (LOG LEVEL: DEBUG)",
         xs=('nº of texts', xs),
         values=[('f string', f_string_ys),
                 ('string format', string_format_ys),
                 ('logging params', logging_params_ys),
                 ('logging checking log level', log_checking_log_level_ys),
                 ('logging using % format', log_using_percent_ys)])
