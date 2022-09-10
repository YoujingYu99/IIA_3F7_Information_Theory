from trees import *
from vl_codes import shannon_fano
from itertools import groupby
from vl_codes import vl_encode, vl_decode
from vl_codes import bytes2bits, bits2bytes
from math import log2
from camzip import camzip
from camunzip import camunzip
from filecmp import cmp
from os import stat
from json import load

f = open("hamlet.txt", "r")
hamlet = f.read()
f.close()

frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(hamlet))])
Nin = sum([frequencies[a] for a in frequencies])
p = dict([(a, frequencies[a] / Nin) for a in frequencies])

from vl_codes import huffman

xt = huffman(p)
print(xtree2newick(xt))

H = lambda pr: -sum([pr[a] * log2(pr[a]) for a in pr])


from camzip import camzip
from camunzip import camunzip

method = "huffman"
filename = "hamlet.txt"

camzip(method, filename)
camunzip(filename + ".cz" + method[0])

from filecmp import cmp
from os import stat
from json import load

Nin = stat(filename).st_size
print(f"Length of original file: {Nin} bytes")
Nout = stat(filename + ".cz" + method[0]).st_size
print(f"Length of compressed file: {Nout} bytes")
print(f"Compression rate: {8.0*Nout/Nin} bits/byte")
with open(filename + ".czp", "r") as fp:
    freq = load(fp)
pf = dict([(a, freq[a] / Nin) for a in freq])
print(f"Entropy: {H(pf)} bits per symbol")
if cmp(filename, filename + ".cuz"):
    print("The two files are the same")
else:
    print("The files are different")


c = xtree2code(xt)
hamlet_huf = vl_encode(hamlet, c)
hamlet_decoded = vl_decode(hamlet_huf, xt)
print("".join(hamlet_decoded[:294]))


# We now introduce a random bit flip
# (bit 400 flipped) in the compressed sequence and observe the result.
hamlet_corrupted = hamlet_huf.copy()
hamlet_corrupted[400] ^= 1
hamlet_decoded = vl_decode(hamlet_corrupted, xt)
print("".join(hamlet_decoded[:297]))
