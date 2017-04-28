#!/usr/bin/env python2.7
import pdb
import unittest
import kfasta
from dnaseqlib import *

###

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)

# @param seq instace of FastaSequence
# @param k integer of length of the subsequence
# return Generator that is basically of [[subsequence_1, hash], [subsequence_2, hash_2]]????
def subsequenceHashes(seq, k):
    print("hi")
    # Create a generator that returns subsequences of length k
    subsequences_generator = kfasta.subsequences(seq, k)

    while True:
        current_subsequence = subsequences_generator.next()
        yield [current_subsequence, hash(current_subsequence)]


    # try:
    #     subseq = ''
    #     while True:
    #         while len(subseq) < k:
    #             subseq += seq.next()
    #         yield subseq
    #         subseq = subseq[1:]
    # except StopIteration:
    #     return
generator = kfasta.FastaSequence("data/fdog0.fa")
sub_hash_generator = subsequenceHashes(generator, 20000)

pdb.set_trace()
