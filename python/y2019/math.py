import functools
from math import *


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def lcmv(l):
    return functools.reduce(lcm, l)
