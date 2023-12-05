"""
experiments with higher dimension basis and checking how to combine them
Should probably be using XOR for higher order modulation, modulo doesn't quite do the right thing when you have more scales.
"""
import itertools
import functools
from operator import xor

def make_basis(n4_times, a=1):
    yield (a,a,a,a)
    for of_idx in range(n4_times-1):
        offset = (0,)*(of_idx*4)
        yield offset + (a,a,0,0,a,a)
        yield offset + (a,0,a,0,a,0,a)
        yield offset + (0,0,0,0,a,a,a,a)
def make_basis2(n16_times, a=1):
    yield (a,)*16
    for of_idx in range(n16_times-1):
        offset = (0,)*(of_idx*16)
        yield offset + ((a,)*8 + (0,)*8)*2
        yield offset + ((a,)*4 + (0,)*4)*4
        yield offset + ((a,)*2 + (0,)*2)*8
        yield offset +  (a,0)*16
        yield offset + (0,)*16+ (a,)*16
print(*make_basis(8,2), sep="\n")
print(*make_basis2(2),sep="\n")

#BB = list(itertools.chain([(1,1,1,1)], make_basis(3), [(1/2,)*16]))
BB_OLD = [(1,1,1,1,0,0,0,0),
      (1,1,0,0,1,1,0,0),
      (1,0,1,0,1,0,1,0),
      (0,0,0,0,1,1,1,1),
      (0,0,0,0,1,1,0,0,1,1),
      (0,0,0,0,1,0,1,0,1,0,1,0),
      (0,0,0,0,0,0,0,0,1,1,1,1)
      ]
#BB = list(itertools.chain(make_basis(8,2), make_basis2(2)))
#BB = list(make_basis(8,2)) # contains 344 combinations of offsets
BB = list(make_basis2(2))
print(*BB, sep="\n\n")
N_dims = max(map(len,BB))
bits_per_dim = len(BB)/N_dims

basis = [b+(0,)*(N_dims-len(b)) for b in BB]
def get_combos(basis):
    # goes over cartesian product of selecting elements from the basis or not
    for selectors in itertools.product([False,True], repeat=len(basis)):
        yield [functools.reduce(xor,v) for v in zip(*itertools.compress(basis,selectors))]
        
power_lookup = {0:0,1:1, 2:4, 3:1}
s = get_combos(basis)
neighbours = 0
for idx,a in enumerate(s):
    if 0<sum(map(power_lookup.__getitem__, a)) <= 16:
        neighbours+=1
        print("{:5d}: {}".format(neighbours,a))
print(neighbours)
exit()





s = list(get_combos(basis))
power = 0
#center_point = (0,)*N_dims
for point in s:
    power += sum(a**2 for a in point)/len(s)
    #center_point = (c+a for c,a in zip(center_point,point))
#center_point = [a/len(s) for a in center_point]
center_point = [sum(a)/len(s) for a in zip(*s)]
print("CENTER IS", center_point)
power -= sum(a**2 for a in center_point)
#print("POWER/dim:", power/N_dims)

print(f"{len(basis)} bits and {power} energy per {N_dims} dims : {bits_per_dim}b/dim, {power/N_dims} pwr/dim")
#assert all(sum(b)==len(b) or sum(b)==0 for b in zip(*s))
for i1,a in enumerate(s):
    for b in s[i1+1:]:
        assert 4<=sum((x-y)**2 for x,y in zip(a,b)), "{a}, {b}".format(a=a,b=b)

print(*sorted(s), sep="\n")
print("works")

test_vec = (0,0,0,1,1,1,1,0)
for vec in s:
    assert 4<=sum((x-y)**2 for x,y in zip(vec,test_vec)), str(vec)
