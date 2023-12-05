"""
seems to be trying to find possible basis vector sets, finding patterns,
pretty sure this is the script that lead to the breakthrough of using
11110000
11001100
10101010 < this one

"""

import itertools

# 7d mapping
dims = 7
count = 4
power = 1
idx_set = itertools.combinations(range(dims), count)

possible_basis_vectors = set()
for idxs in idx_set:
    b = [0]*dims
    for i in idxs:
        b[i] = power
    possible_basis_vectors.add(tuple(b))

print(*possible_basis_vectors, sep="\n")
print(len(possible_basis_vectors))

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def check(already_chosen):
    
    for new_option in possible_basis_vectors-already_chosen:
        if all(dot(new_option, x)==2 for x in already_chosen):
            new_set = already_chosen|{new_option}
            if len(new_set)==dims:
                #assert all(sum(x)==4 for x in zip(*new_set))
                print(*sorted(new_set),sep="\n")
                print("\n\n\n")
            else:
                check(already_chosen|{new_option})

check({(0,0,0,1,1,1,1)})
