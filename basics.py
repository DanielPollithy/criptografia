from random import randint
from books import _1984

# https://en.wikipedia.org/wiki/Letter_frequency
import math

FREQ_ENG = {
    "a": 0.08167,
    "b": 0.01492,
    "c": 0.02782,
    "d": 0.04253,
    "e": 0.12702,
    "f": 0.02228,
    "g": 0.02015,
    "h": 0.06094,
    "i": 0.06966,
    "j": 0.00153,
    "k": 0.00772,
    "l": 0.04025,
    "m": 0.02406,
    "n": 0.06749,
    "o": 0.07507,
    "p": 0.01929,
    "q": 0.00095,
    "r": 0.05987,
    "s": 0.06327,
    "t": 0.09056,
    "u": 0.02758,
    "v": 0.00978,
    "w": 0.02360,
    "x": 0.00150,
    "y": 0.01974,
    "z": 0.00074
}


def get_frequency(text):
    freq = {a: 0 for a in set(text)}
    for c in text:
        freq[c] += 1
    for a in freq.keys():
        freq[a] /= len(text)
    return freq



class ALPHABET:
    letters = "abcdefghijklmnopqrstuvwxyz" # "".join([chr(i) for i in range(0, 255)])

    @classmethod
    def num_to_chr(cls, n):
        return cls.letters[n % cls.n()]

    @classmethod
    def chr_to_num(cls, c):
        return cls.letters.index(c.lower())

    @classmethod
    def n(cls):
        return len(cls.letters)

    @classmethod
    def clear_text(cls, text):
        new_text = ""
        for c in text:
            if c in cls.letters:
                new_text += c
        return new_text

_1984 = ALPHABET.clear_text(_1984)

# Basic methods

# algoritmo de euclides para obtener el maximo comun divisor mcd de dos enteros
def mcd(a, b):
    while b > 0:
        r = a % b
        a = b
        b = r
    return a


# minimo comun multiplo mcm
# mcd(a,b) * mcm(a,b) = a*b
# mcm(a,b) = a*b/mcd(a,b)
def mcm(a, b):
    return a * b / mcd(a, b)


# algoritmo extendido euclido
def algoritmo_extendido_euclides(a_, b_, log=False):
    a = [a_]
    b = [b_]
    q = [a_ / b_]
    r = [a_ % b_]
    x = []
    y = []
    i = 1
    while r[-1] > 0:
        a.append(b[-1])
        b.append(r[-1])
        q.append(a[-1] / b[-1])
        r.append(a[-1] % b[-1])
        i += 1
    d = b[-1]
    x.append(0)
    y.append(1)
    i -= 1
    while i > 0:
        x.append(y[-1])
        y.append(x[-2] - (y[-1] * q[i - 1]))

        i -= 1
    x.reverse()
    y.reverse()
    if log:
        print("a\tb\tq\tr\tx\ty")
        print("-" * 80)
        for i in range(len(x)):
            print("{}\t{}\t{}\t{}\t{}\t{}".format(a[i], b[i], q[i], r[i], x[i], y[i]))

    return (d, x[0], y[0])


# Usar la igualidad de Bezout para calcular d = e^-1 mod n
# d * e + k * n = mcd(e, n) = 1
def inverso_multiplicativo(e, n, log=False):
    mcd, d, k = algoritmo_extendido_euclides(e, n, log=log)
    assert mcd == 1
    if log:
        print("{} * {} + {} * {} = {} ".format(d, e, k, n, (d * e + k * n)))
    return d


# prime test
def is_prime(n):
    if n in (1, 2, 3, 5, 7, 11, 13):
        return True
    x = (n / 2) + 1
    t = 2
    while t <= x:
        if n % t == 0:
            return False
        t += 1
    return True


def prime_factorization(n):
    if is_prime(n):
        return [n]
    a = 2
    primes = []
    while n > 1:
        if n % a == 0:
            primes.append(a)
            n /= a
            if is_prime(n):
                primes.append(int(n))
                break
        else:
            a += 1
    return primes


def is_sqrt(n):
    last_two = n%100
    return last_two in (0, 1, 21, 41, 61, 81, 4, 24, 44, 64, 84, 25,
                        16, 36, 56, 76, 96, 9, 29, 49, 69, 89)


def fermat_factorization(n):
    if is_prime(n):
        return None
    x = int(math.ceil(math.sqrt(n)))
    r = x**2 - n
    if r == 0:
        return x
    while not is_sqrt(int(r)):
        r += 2*x + 1
        x += 1
    y = math.sqrt(r)
    a = x+y
    b = x-y
    return a, b



def p(c, text):
    """
    La probabilidad de un caracter c en un texto p
    :param c: string con solo un character
    :param text: string
    :return: float
    """

    return text.count(c)/len(text)


def IC(T1, T2=None):
    if not T2:
        T2 = T1
    valor = 0
    T = set(T1+T2)
    for c in T:
        valor += p(c, T1) * p(c, T2)
    return valor


def miller_rabin_test(n):
    pass




# from books import _1984
# print(IC(_1984, _1984))
# print(IC("a"*100, "a"*100))
# import random
# al = "".join([chr(random.randint(1, 255)) for c in range(100000)])
# print(IC(al, al))


# for i in range(100):
#    print(i, prime_factorization(i))


#for i in range(100, 200):
#    print(fermat_factorization(i))