#!/usr/bin/env python2.7
import pdb
import unittest
import kfasta
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.single_dict = {}
        for pair in pairs:
            self.put(pair[0], pair[1])

    # Associates the value v with the key k.
    def put(self, k, v):
        if k not in self.single_dict:
            self.single_dict[k] = []

        self.single_dict[k].append(v)

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        if k not in self.single_dict:
            self.single_dict[k] = []

        return self.single_dict[k]

multidict = Multidict([("liann", "is nice")])

multidict.put("cats", "spots")
multidict.put("dogs", "lol")
multidict.put("cats", "bob")

print(multidict.get("liann"))
print(multidict.get("cats"))
print(multidict.get("dogs"))
# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)

# @param seq instace of FastaSequence
# @param k integer of length of the subsequence
# return Generator that is basically of [[str_subsequence_1, hash], [str_subsequence_2, hash_2]]????
def subsequenceHashes(seq, k):
    # Begin create an initial sequence of length k
    current_sequence = ""

    for i in range(k):
        current_sequence += seq.next()

    location = 0
    rolling_hash = RollingHash(current_sequence)
    # yield (current_sequence, rolling_hash.current_hash())
    yield (rolling_hash.current_hash(), current_sequence, location)
    # End create an initial sequence of length k

    # Almost(endlessly) iterate through the sequence till the end
    try:
        while True:
            next_char = seq.next()
            location += 1
            rolling_hash.slide(current_sequence[0], next_char)
            current_sequence = current_sequence[1:] + next_char
            # yield (current_sequence, rolling_hash.current_hash())
            yield (rolling_hash.current_hash(), current_sequence, location)
    except StopIteration:
        return

generator = kfasta.FastaSequence("data/ftest0.fa")
sub_generator = subsequenceHashes(generator, 50)

for thing in sub_generator:
    print thing

# pdb.set_trace()


# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    raise Exception("Not implemented!")
    # Begin create an initial sequence of length k
    current_sequence = ""

    for i in range(k):
        current_sequence += seq.next()

    location = 0
    rolling_hash = RollingHash(current_sequence)
    # yield (current_sequence, rolling_hash.current_hash())
    yield (rolling_hash.current_hash(), current_sequence, location)
    # End create an initial sequence of length k

    # Almost(endlessly) iterate through the sequence till the end
    try:
        while True:
            next_char = seq.next()
            location += 1
            rolling_hash.slide(current_sequence[0], next_char)
            current_sequence = current_sequence[1:] + next_char
            # yield (current_sequence, rolling_hash.current_hash())
            yield (rolling_hash.current_hash(), current_sequence, location)
    except StopIteration:
        return

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
#
# subsequence_and_hash = (hash, subseq, location)
# val_and_loc = (subseq, location)
def getExactSubmatches(a, b, k, m):
    a_subsequence_generator = subsequenceHashes(a, k)
    b_subsequence_generator = subsequenceHashes(b, k)

    multidict = Multidict()
    # Add all submatches in a to the multidict
    for subsequence_and_hash in a_subsequence_generator:
        multidict.put(subsequence_and_hash[0], (subsequence_and_hash[1], subsequence_and_hash[2]))
        print("in putting in a thing")
        print(subsequence_and_hash[1], subsequence_and_hash[2])

    # Check to see if the length of the multidict is more than 1, if so, add to submatches
    for subsequence_and_hash in b_subsequence_generator:
        b_val_to_check = subsequence_and_hash[1]
        b_loc = subsequence_and_hash[2]

        val = multidict.get(subsequence_and_hash[0])
        if len(val) is not 0:
            print "I found a key/hash match, checking for collisions"

            for val_and_loc in val:
                # IF it's a real hash match
                if val_and_loc[0] == b_val_to_check:
                    yield (val_and_loc[1], b_loc)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
