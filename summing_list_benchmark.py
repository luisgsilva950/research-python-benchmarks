import json
import random
from typing import List
from functools import reduce

from utils import timeit, plot, moving_average


class MyObject:
    def __init__(self, x):
        self.x = x


def generate_list_of_objects(size: int):
    return [MyObject(random.randint(1, 100)) for _ in range(size)]


@timeit(executions=5)
def sum_using_for_loop(objects: List[MyObject]):
    total = 0
    for obj in objects:
        total += obj.x
    return total


@timeit(executions=5)
def sum_using_map(objects: List[MyObject]):
    return sum(map(lambda obj: obj.x, objects))


@timeit(executions=5)
def sum_using_list_comprehension(objects: List[MyObject]):
    return sum(obj.x for obj in objects)


@timeit(executions=5)
def sum_using_reduce(objects: List[MyObject]):
    return reduce(lambda acc, obj: acc + obj.x, objects, 0)


if __name__ == '__main__':
    xs = []
    for_loop_ys, map_ys, list_comprehension_ys, reduce_ys = [], [], [], []

    for x in range(1, 20000, 200):
        xs.append(x)
        object_list = generate_list_of_objects(size=x)

        for_loop_ys.append(sum_using_for_loop(objects=object_list))
        print(sum_using_for_loop.__name__, x, for_loop_ys[-1])

        map_ys.append(sum_using_map(objects=object_list))
        print(sum_using_map.__name__, x, map_ys[-1])

        list_comprehension_ys.append(sum_using_list_comprehension(objects=object_list))
        print(sum_using_list_comprehension.__name__, x, list_comprehension_ys[-1])

        reduce_ys.append(sum_using_reduce(objects=object_list))
        print(sum_using_reduce.__name__, x, reduce_ys[-1])

    results = {"xs": xs,
               "for_loop_ys": for_loop_ys,
               "map_ys": map_ys,
               "list_comprehension_ys": list_comprehension_ys,
               "reduce_ys": reduce_ys}

    with open("results/python_sum_objects.json", "w") as fp:
        json.dump(results, fp=fp)

    plot(title="Comparison of summing methods using Python 3.10",
         xs=('nº objects', xs),
         values=[('for loop', moving_average(for_loop_ys)),
                 ('map', moving_average(map_ys)),
                 ('list comprehension', moving_average(list_comprehension_ys)),
                 ('reduce', moving_average(reduce_ys))])
