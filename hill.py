import random

__author__ = 'Daniel'

def generate_key(n):
    while True:
        k = [[random.randint(0, 255) for y in range(n)] for x in range(n)]
        k_r = key_inverse(k)
        if k_r:
            return k, k_r

def key_inverse(k):
    # algorithm to inverse matrix...
    pass