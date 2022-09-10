from trees import *
from vl_codes import shannon_fano
from random import random


p = [random() for k in range(16)]
p = dict([(chr(k + ord("a")), p[k] / sum(p)) for k in range(len(p))])
print(f"Probability distribution: {p}\n")
c = shannon_fano(p)
print(f"Codebook: {c}\n")
xt = code2xtree(c)
print(f"Cut and paste for phylo.io: {xtree2newick(xt)}")
