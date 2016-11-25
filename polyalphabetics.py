from basics import mcd, _1984, ALPHABET, prime_factorization
from collections import Counter
from monoalphabetics import get_shift_by_frequency

def viginere(text, key, alphabet="abcdefghijklmnopqrstuvwxyz", log=False):
    text = text.lower()
    key = key.lower()
    key_size = len(key)
    cipher_text = []

    def char_to_num(c):
        return alphabet.find(c)

    def num_to_char(n):
        return alphabet[n % len(alphabet)]

    for i in range(0, len(text), key_size):
        for offset in range(0, key_size):
            x = i+offset
            if x >= len(text):
                break
            k = char_to_num(key[offset])
            c = char_to_num(text[x])
            cipher_text.append(num_to_char(k+c))
            if log:
                print("{} ({}) \t+ {} ({}) \t= {} ({})".format(
                    key[offset], k, text[x], c, cipher_text[-1], (k+c) % len(alphabet)
                ))
    return "".join(cipher_text)




def kasiki_distances(cipher_text, max_block_size=50, min_block_size=3):
    block_size = min(int(len(cipher_text)/2), max_block_size)
    while block_size >= min_block_size:
        print(block_size)
        for i in range(0, len(cipher_text)-block_size+1):
            block = cipher_text[i:i+block_size]
            if cipher_text.count(block) > 2:
                occs = []
                index = 0
                while index < len(cipher_text):
                    index = cipher_text.find(block, index, len(cipher_text))
                    if index == -1:
                        break
                    occs.append(index)
                    index += block_size
                distances = {}
                for a in occs:
                    for b in occs:
                        if a == b:
                            pass
                        else:
                            distances[(a, b)] = max(a, b)-min(a, b)
                return block, distances
        block_size -= 1


def get_key_sizes(distances):
    d = list(distances[1].values())
    mcds = []
    for i in range(0, len(d)-1):
        mcds.append(mcd(d[i], d[i+1]))
    key_sizes = []
    for m in mcds:
        key_sizes += prime_factorization(m)
        # print(key_sizes)
    counter = Counter(key_sizes)
    return sorted(counter, key=counter.get, reverse=True)


def break_viginere_key(text, keysize, alphabet=ALPHABET, log=False):
    columns = ["" for _ in range(keysize)]
    i = 0
    for c in text:
        columns[i] += c
        i = (i+1) % keysize
    mono_shifts = []
    for c in columns:
        mono_shifts.append(get_shift_by_frequency(c))  # TODO: use IC here
        if log:
            print(mono_shifts)
    guess = ""
    for m in mono_shifts:
        guess += ALPHABET.num_to_chr(m[0])
    return guess, mono_shifts



def test_vigenere():
    a = viginere(_1984, "clave")
    b = kasiki_distances(a, max_block_size=20)
    c = get_key_sizes(b)

    print(b)
    print(c)

    for x in c:
        d = break_viginere_key(a, x)
        print(d)




