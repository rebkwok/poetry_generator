#!/usr/bin/env python3
# encoding: utf-8

import sys
from pprint import pprint
from random import choice

EOS = ['.', '?', '!']


def build_dict(words):
    """
    Build a dictionary from the words.

    (word1, word2) => [w1, w2, ...]  # key: tuple; value: list
    """
    d = {}
    syllD = {}
    for i, word in enumerate(words):
        if word not in syllD:
            syllD[word] = syllables(word)
        try:
            first, second, third = words[i], words[i+1], words[i+2]
        except IndexError:
            break
        key = (first, second)
        if key not in d:
            d[key] = []
        #
        d[key].append(third)

    if words[-1] not in syllD:
        syllD[words[-1]] = syllables(words[-1])

    if words[-2] not in syllD:
        syllD[words[-2]] = syllables(words[-2])


    return (d,syllD)


def generate_sentence(d, syllD, length, seed = None, end = False):
    if not seed:
        li = [key for key in d.keys() if key[0][0].isupper()]
        key = choice(li)
    else:
        key = seed

    li = []
    first, second = key
    syllableCount = 0
    if not seed:
        syllableCount = syllD[first] + syllD[second]
        li.append(first)
        li.append(second)
    while True:
        try:
            if end and syllableCount > length - 3:
                ends = list(filter(lambda x: x[-1] in EOS, d[key]))
                    s = syllD[value]
                    if value[-1] in EOS and syllableCount + s > length:
                        third = value
                        break
            third = choice(d[key])
        except KeyError:
            break
        li.append(third)
        syllableCount += syllD[third]
        if syllableCount >= length:
            break
        # else
        key = (second, third)
        first, second = key

    return ' '.join(li)

def syllables(word):
    count = 0
    vowels = 'aeiouy'
    wordstriped = word.lower().strip(".:;?!")

    if wordstriped != '': word = wordstriped

    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count


def main():
    fname = sys.argv[1]
    with open(fname, "rt", encoding="utf-8") as f:
        text = f.read()

    words = list(filter(lambda x: x != '', text.split()))
    d, syllD = build_dict(words)

    line = generate_sentence(d, syllD, 9)
    print(line)
    line = generate_sentence(d, syllD, 9, tuple(line.split(' ')[-2:]))
    print(line + '.')
    line = generate_sentence(d, syllD, 4)
    print(line)
    line = generate_sentence(d, syllD, 4, tuple(line.split(' ')[-2:]))
    print(line)
    line = generate_sentence(d, syllD, 9, tuple(line.split(' ')[-2:]))
    print(line)


####################

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: provide an input corpus file.")
        sys.exit(1)
    # else
    main()
