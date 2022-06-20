#!/home/cflor/.asdf/shims/python


import math
import os
import random
import re
import sys
from dateutil.parser import *

def time_delta(t1, t2):
    return abs(parse(t1).timestamp() - parse(t2).timestamp())    

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        t1 = str(input())
        t2 = str(input())

        delta = round(time_delta(t1, t2))
        print(delta)

