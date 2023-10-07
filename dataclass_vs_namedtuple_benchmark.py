import json
from collections import namedtuple
from dataclasses import dataclass

from utils import timeit, plot

NamedA = namedtuple('NameA', 'a b c')


@dataclass
class DataclassA:
    a: int
    b: int
    c: int


@dataclass(frozen=True)
class FrozenDataclassA:
    a: int
    b: int
    c: int


class NormalA:
    a: int
    b: int
    c: int

    def __init__(self, *args, **kwargs):
        self.a = kwargs["a"]
        self.b = kwargs["b"]
        self.c = kwargs["c"]


@timeit(executions=200)
def instantiating_dataclass(x: int):
    r = []
    for _ in range(x):
        r.append(DataclassA(a=0, b=1, c=2))


@timeit(executions=200)
def instantiating_frozen_dataclass(x: int):
    r = []
    for _ in range(x):
        r.append(FrozenDataclassA(a=0, b=1, c=2))


@timeit(executions=200)
def instantiating_namedtuple(x: int):
    r = []
    for _ in range(x):
        r.append(NamedA(a=0, b=1, c=2))


@timeit(executions=200)
def instantiating_python_class(x: int):
    r = []
    for _ in range(x):
        r.append(NormalA(a=0, b=1, c=2))


if __name__ == '__main__':
    xs = []
    named_tuple_ys, dataclass_ys, pythonclass_ys, frozen_dataclass_ys = [], [], [], []
    for x in range(1, 2000, 100):
        xs.append(x)
        named_tuple_ys.append(instantiating_namedtuple(x=x))
        print(instantiating_namedtuple.__name__, x, named_tuple_ys[-1])
        dataclass_ys.append(instantiating_dataclass(x=x))
        print(instantiating_dataclass.__name__, x, dataclass_ys[-1])
        pythonclass_ys.append(instantiating_python_class(x=x))
        print(instantiating_python_class.__name__, x, pythonclass_ys[-1])
        frozen_dataclass_ys.append(instantiating_frozen_dataclass(x=x))
        print(instantiating_frozen_dataclass.__name__, x, frozen_dataclass_ys[-1])

    results = {"xs": xs,
               "named_tuple_ys": named_tuple_ys,
               "dataclass_ys": dataclass_ys,
               "pythonclass_ys": pythonclass_ys,
               "frozen_dataclass_ys": frozen_dataclass_ys}

    with open("python_instantiating_object_ways.json", "w") as fp:
        json.dump(results, fp=fp)

    plot(title="Comparison of instantiating objects using Python 3.10",
         xs=('nº of objects', xs),
         values=[('namedtuple', named_tuple_ys),
                 ('dataclass', dataclass_ys),
                 ('pythonclass', pythonclass_ys),
                 ('frozen_dataclass', frozen_dataclass_ys)])
