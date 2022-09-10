from trees import *
from vl_codes import shannon_fano

f = open("hamlet.txt", "r")
hamlet = f.read()
f.close()

from itertools import groupby

frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(hamlet))])
Nin = sum([frequencies[a] for a in frequencies])
p = dict([(a, frequencies[a] / Nin) for a in frequencies])
print(p)

c = shannon_fano(p)
# print(c)
xt = code2xtree(c)
# print(len(xt))
# print('xt', xt[:10])
# print(xtree2newick(xt))
# print(len(c['&']))


from vl_codes import vl_encode

hamlet_sf = vl_encode(hamlet, c)
print(f"Length of binary sequence: {len(hamlet_sf)}")

from vl_codes import bytes2bits, bits2bytes

x = bits2bytes([0, 1])
print([format(a, "08b") for a in x])
y = bytes2bits(x)
print(f"The original bits are: {y}")
print(bits2bytes([0, 1, 1, 0, 1, 1, 0, 0, 0]))

hamlet_zipped = bits2bytes(hamlet_sf)
Nout = len(hamlet_zipped)
print(f"Length of compressed string: {Nout}")


print(f"Compression ratio (rateless): {Nout/Nin}")
print(f"Compression ratio (bits per byte): {8.0*Nout/Nin}")


from math import log2

H = lambda pr: -sum([pr[a] * log2(pr[a]) for a in pr])
print(f"Entropy: {H(p)}")


from vl_codes import vl_decode

xt = code2xtree(c)
hamlet_unzipped = vl_decode(hamlet_sf, xt)
print(f"Length of unzipped file: {len(hamlet_unzipped)}")

# print(''.join(hamlet_unzipped[:294]))


from camzip import camzip
from camunzip import camunzip

method = "shannon_fano"
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
