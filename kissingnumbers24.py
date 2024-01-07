"""
finds kissing number for 24 dim lattice

goes over every possible combination of the first order modulation and checks if it matches any of the 3 options for 2nd order
modulation and adds it to the count, 
"""

import itertools
import collections
from operator import xor
from functools import reduce, partial

xor_list = partial(reduce, xor) # will use this for map(xor_list, every_combination(...))


bases = [
    0b000000000000000000001111,
    0b000000000000000000110011,
    0b000000000000000001010101,
    0b000000000000000011110000,
    0b000000000000001100110000,
    0b000000000000010101010000,
    0b000000000000111100000000,
    0b000000000011001100000000,
    0b000000000101010100000000,
    0b000000001111000000000000,
    0b000000110011000000000000,
    0b000001010101000000000000,
    0b000011110000000000000000,
    0b001100110000000000000000,
    0b010101010000000000000000,
    0b111100000000000000000000,
    0b000100010001000100000000,
    0b000100010000000000010001,
]
N = max(map(len, map("{:b}".format, bases)))


bases2 = [
    # <04><08><12><16><20><24>
    0b111111111111111100000000,
    0b111111110000000011111111,
    # for this script we use the 3 possible combinations of non 0 2nd order modulation
    # since setting both bits of above vectors is just as useful to us.
    0b000000001111111111111111,
]

B = collections.namedtuple("B",["data","idxset"])

distance_vectors = [B(a,frozenset([i])) for i,a in enumerate(bases)]

def count_ones(num):
    return bin(num).count("1")

def every_combination(things, min_length=1):
    """yields every combination of every length from the set of things, setting min_length to 0 also includes the empty set"""
    for length in range(min_length, len(things)+1):
        yield from itertools.combinations(things, length)


total = N*2 # for moving +- any single dimension

# for spot_in_list, vec1 in enumerate(distance_vectors):
#     # the spot in list of the second vector isn't needed but left enumerate to make
#     # it easier to get later if needed.
#     for (_, vec2) in itertools.islice(enumerate(distance_vectors),spot_in_list+1,None):
#         if vec1.idxset & vec2.idxset:
#             continue
#         # here we are explicitly checking that there are exactly 4 non zero entries, which would need to be generalized later
#         if count_ones(vec1.data ^ vec2.data)==4:
#             distance_vectors.append(B(vec1.data ^ vec2.data, vec1.idxset|vec2.idxset))

# distance_set = set(distance_vectors)

# print("list:",len(distance_vectors), "set:",len(distance_set))

# since we can have any variation of +- for each of 4 entries we get 16 times the movement

# total += len(distance_set)*16

for dir_vec in map(xor_list, every_combination(bases)):
    # for every possible direction we move in 1st order modulation, check if it is a subset of 1s from the 3 viable 2nd order
    # modulation directions, if it is we have another viable neighbour
    for base2nd in bases2:
        # the bits in common will be equal to the one with fewer bits when it is a subset.
        if dir_vec & base2nd == dir_vec:
            # TODO: I think this double counts some distance vectors,
            # it adds 2 to account for negative distances but there are some I think the negative is already counted by different bit flips but I'm not totally sure.
            total+=2 
    if count_ones(dir_vec) == 4:
        total += 16 # for all possible +- of those 4 bits by toggling 0th order modulation

        
print("TENTATIVE RESULT")
print("I'm not totally confident this is calculating it correctly")

print(total)
            
        
        
