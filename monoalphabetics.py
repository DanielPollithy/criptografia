from collections import defaultdict

__author__ = 'Daniel'

from basics import ALPHABET, IC, _1984, FREQ_ENG, get_frequency


def caesar(text, shift, alphabet=ALPHABET):
    new_text = ""
    for c in text:
        new_text += ALPHABET.num_to_chr( ALPHABET.chr_to_num(c) + shift )
    return new_text


def get_shift_by_ic(cipher_text, alphabet=ALPHABET, ic=0.0667):
    highest = [-1, -1]
    for i in range(0, alphabet.n()):
        ic = IC(caesar(cipher_text, -i, alphabet=alphabet))
        if ic >= highest[1]:
            highest = [i, ic]
    return highest[0]


def get_shift_by_frequency(cipher_text, freq=FREQ_ENG, alphabet=ALPHABET, log=False):
    frequency = get_frequency(cipher_text)
    freq_sort = sorted(freq, key=freq.get, reverse=False)
    diff = defaultdict(int)
    for i, w in enumerate(sorted(frequency, key=frequency.get, reverse=False)):
        s = (alphabet.chr_to_num(w) - alphabet.chr_to_num(freq_sort[i])) % 26
        diff[s] += 1
        if log:
            print("{}[{}] - {} = {}".format(w, frequency[w], freq_sort[i], s))
    return sorted(diff, key=diff.get, reverse=True)


def test_mono():
    print(caesar("HALLOWELT", 3))
    print(caesar(caesar("HALLOWELT", 3), -3))
    a = caesar(_1984, 17)
    b = get_shift_by_ic(a)
    c = get_shift_by_frequency(a)
    print(b)
    print(c)
    print(caesar(a[0:100], -c[0]))
