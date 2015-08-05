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
    syll_d = {}
    for i, word in enumerate(words):
        if word not in syll_d:
            syll_d[word] = syllables(word)
        try:
            first, second, third = words[i], words[i+1], words[i+2]
        except IndexError:
            break
        key = (first, second)
        if key not in d:
            d[key] = []
        #
        d[key].append(third)

    if words[-1] not in syll_d:
        syll_d[words[-1]] = syllables(words[-1])

    if words[-2] not in syll_d:
        syll_d[words[-2]] = syllables(words[-2])


    return (d,syll_d)


def generate_line(d, syll_d, length, seed = None, end = False):
    if not seed:
        li = [key for key in d.keys() if key[0][0].isupper()]
        key = choice(li)
    else:
        key = seed

    li = []
    first, second = key
    syllable_count = 0
    if not seed:
        syllable_count = syll_d[first] + syll_d[second]
        li.append(first)
        li.append(second)
    while True:
        try:
            third = choice(d[key])
        except KeyError:
            break
        li.append(third)
        syllable_count += syll_d[third]
        if syllable_count >= length:
            break
        # else
        key = (second, third)
        first, second = key

    return ' '.join(li)

def syllables(word):
    count = 0
    vowels = 'aeiouy'
    wordstripped = word.lower().strip(".:;?!")

    if wordstripped != '': word = wordstripped

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
    d, syll_d = build_dict(words)

    line1 = generate_line(d, syll_d, 9)
    line2 = generate_line(d, syll_d, 9, tuple(line1.split(' ')[-2:]))
    line3 = generate_line(d, syll_d, 4)
    line4 = generate_line(d, syll_d, 4, tuple(line3.split(' ')[-2:]))
    line5 = generate_line(d, syll_d, 9, tuple(line4.split(' ')[-2:])) + choice(EOS)

    poem = [line1, line2, line3, line4, line5]
    print('\n'.join(poem))


####################

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: provide an input corpus file.")
        sys.exit(1)
    # else
    main()
