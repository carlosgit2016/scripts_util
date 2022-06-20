#!/home/cflor/.asdf/shims/python


import math
import os
import random
import re
import sys
from dateutil.parser import *

def flip_negative_bit(n):
    b = str(bin(n)).replace('-', '')
    return int(b, base=0)

def time_delta(t1, t2):
    d = flip_negative_bit(parse(t1).timestamp() - parse(t2).timestamp())
    return d

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        t1 = str(input())
        t2 = str(input())

        delta = round(time_delta(t1, t2))
        print(delta)

