"""

finds 4320 neighbours

finds kissing number for lattice in 16D, ends up being exactly equivelent to the 6th configuration from the listed ones at:
https://cohn.mit.edu/sites/default/files/documents/16d-kissing.txt

in 16D since the second order modulation toggles every dimension it means every possible result from the first order modulation
is a subset and therefore can generate a valid neighbour, in 24D we'd have to go over every possibility manually and see if it
is a subset of the bits flipped from any of the 3 possible alternatives from the second order modulation and only count those
for neighbours that make use of 2nd order modulation. 
"""

import itertools
import collections

PRINT_ALL_VECTORS = False
if PRINT_ALL_VECTORS: input("print all vectors was set to true but that was not properly implmeneted for second order neighbours, enter to continue")
N = 16
S = 1

bases = [
    0b0000000000001111,
    0b0000000000110011,
    0b0000000001010101,
    0b0000000011110000,
    0b0000001100110000,
    0b0000010101010000,
    0b0000111100000000,
    0b0011001100000000,
    0b0101010100000000,
    0b1111000000000000,
    0b0001000100010001]

B = collections.namedtuple("B",["data","idxset"])

distance_vectors = [B(a,frozenset([i])) for i,a in enumerate(bases)]

def count_ones(num):
    return bin(num).count("1")

if PRINT_ALL_VECTORS:
    for i in range(N):
        vec = [0]*N
        vec[i] = 2**S
        print(vec)
        vec[i]*=-1
        print(vec)

total = N*2 # for moving +- any single dimension

for spot_in_list, vec1 in enumerate(distance_vectors):
    if PRINT_ALL_VECTORS:
        print(bin(vec1.data), vec1.idxset)
    # the spot in list of the second vector isn't needed but left enumerate to make
    # it easier to get later if needed.
    for (_, vec2) in itertools.islice(enumerate(distance_vectors),spot_in_list+1,None):
        if vec1.idxset & vec2.idxset:
            continue
        # here we are explicitly checking that there are exactly 4 non zero entries, which would need to be generalized later
        if count_ones(vec1.data ^ vec2.data)==4:
            distance_vectors.append(B(vec1.data ^ vec2.data, vec1.idxset|vec2.idxset))

distance_set = set(distance_vectors)

print("list:",len(distance_vectors), "set:",len(distance_set))

# since we can have any variation of +- for each of 4 entries we get 16 times the movement

total += len(distance_set)*16

# we can also apply the second order modulation where all 16 dimensions are moved a bit
# and then we take any viable permutation of the 1st order modulation and back up by that amount
# (alternatively move forward by 1st modulation and then move backwards by 0th modulation, is equivelent)
# and that gives another valid neighbour

total += 2**len(bases)

print(total)
            
        
        
