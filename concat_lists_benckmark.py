import json
from typing import List, Any

from utils import timeit, plot

ITEMS = [dict(foo=f"This is dummy data {u + 1}") for u in range(1000)]


def generate_list_of_x_lists(size: int):
    values = []
    for i in range(size):
        values.append(ITEMS.copy())
    return values


@timeit(executions=1)
def concat_using_sum_time(values: List[List[Any]]):
    return sum(values, [])


@timeit(executions=1)
def concat_using_plus_operator_time(values: List[List[Any]]):
    result = []
    for v in values:
        result += v
    return result


@timeit(executions=1)
def concat_using_extend_time(values: List[List[Any]]):
    result = []
    for v in values:
        result.extend(v)
    return result


@timeit(executions=1)
def concat_using_list_compression(values: List[List[Any]]):
    return [i for vv in values for i in vv]


if __name__ == '__main__':
    xs = []
    sum_ys, plus_operator_ys, extend_ys, compression_ys = [], [], [], []
    for x in range(1, 2000, 200):
        xs.append(x)
        compressed_values = generate_list_of_x_lists(size=x)
        sum_ys.append(concat_using_sum_time(values=compressed_values))
        print(concat_using_sum_time.__name__, x, sum_ys[-1])
        plus_operator_ys.append(concat_using_plus_operator_time(values=compressed_values))
        print(concat_using_plus_operator_time.__name__, x, plus_operator_ys[-1])
        extend_ys.append(concat_using_extend_time(values=compressed_values))
        print(concat_using_extend_time.__name__, x, extend_ys[-1])
        compression_ys.append(concat_using_list_compression(values=compressed_values))
        print(concat_using_list_compression.__name__, x, compression_ys[-1])

    results = {"xs": xs,
               "sum_ys": sum_ys,
               "plus_operator_ys": plus_operator_ys,
               "extend_ys": extend_ys,
               "compression_ys": compression_ys}

    with open("results/python_concat_lists.json", "w") as fp:
        json.dump(results, fp=fp)

    plot(title="Comparison of flat lists methods using Python 3.10",
         xs=('nº lists', xs),
         values=[('plus operator', plus_operator_ys),
                 ('sum', sum_ys),
                 ('extend', extend_ys),
                 ('list comprehension', plus_operator_ys)])
