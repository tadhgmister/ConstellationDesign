"""
finds all possible distance vectors for a given constellation.
For a given set of basis vectors that are combined XORed, the set of points in the constellation is any combination of them
The distance vectors are therefore the vector difference between any 2 points in the constellation, however by the original construction this corresponds to just taking the set of basis vectors where some may be negated
so all possible distance vectors is the set of (-1,0,1) applied to every basis vector, except that isn't super well defined if they are created with xor

need to figure it out

pilimiary ideas are to do similar to test2 where I have some notion of sorting the basis vectors, whenever I do a subtraction I always keep the "bigger" one positive by the sorting metric so that everything stays "positive" but I need to define that more precisely.

Second is that |a-b| = a.a - 2a.b + b.b, if we want the biggest of |a-b| or |a+b| we just do -2*abs(a.b), we want cases where |a-b|^2 = min distance which should be a.a and b.b, although that requirement will be dropped at some point. This means that a.a + b.b - 2*abs(a.b) is the "energy" of the distance vector, if we have a.a=b.b=|a-b|^2 = X we'd have X = 2X-2abs(a.b), 2abs(a.b) = 2X-X, abs(a.b) = X. We will ned some clever way to iterate over the combinations since A-B may not be a useful vector but A-B+C could, but if we just add newly found vectors to a set we will end up checking stuff like A+A-B which we don't want. Can probably just keep a map of basis vectors to their coefficients (-1 or 1) and only test vectors if their constructed basis are disjoint. 

We can go over every pairwise set of basis vectors to find comboes that result in the same distance,

So I messed up. I still need to be applying the sum and difference modulo somehow, the last 2 basis vectors shouldn't be able to get to the point (4,4,2,2,2,2) on their own so I'd end up needing to apply the (4,0,0,..) basis twice with both basis vectors to get a valid point in our constellation.

The other option is to consider the distance wrapped around which would be the case if we added higher order QAM or looked at a starting point in opposite direction, wait but isn't the opposite direction already accounted for?

Idk I need to sleep.
"""
import itertools

def is_useful_metric(vec_len_2):
    """returns whether a vector should be kept in the set of vectors we are tracking"""
    return True

bases_TUPLES = sorted([
    (4,0,0,0,0,0),
    (0,4,0,0,0,0),
    (0,0,4,0,0,0),
    (0,0,0,4,0,0),
    (0,0,0,0,4,0),
    (0,0,0,0,0,4),
    (2,2,2,2,0,0),
    (2,2,0,0,2,2)
])
class Vector: #(tuple):
    __slots__ = ["elems","len_2", "basis_map"]
    def __init__(self, data, basis_map, len_2=None, order="IGNORED"):
        #super().__init__(*data)
        self.elems = tuple(data)
        self.len_2 = len_2 if len_2 is not None else sum(a**2 for a in data)
        #self.order = order
        self.basis_map = basis_map
    @property
    def order(self):
        import warnings
        warnings.warn("order is deprecated stop using it")
        return 0
SEEN = set(bases_TUPLES)
bases = [None]*len(bases_TUPLES)
for idx,elem in enumerate(bases_TUPLES):
    bases[idx] = Vector(elem, order=idx, basis_map={idx:1})
    print(bases[idx].elems)


for idx,base in enumerate(bases):
    for other in itertools.islice(bases, idx+1,None):
        #print(base.basis_map.keys() & other.basis_map.keys())
        if base.basis_map.keys() & other.basis_map.keys():
            continue # vectors use common distance vectors,
            # their sum or difference will either cancel out so it will be redundant with another vector we already calculated
            # or it will drift more than 2 vectors worth which is not useful for adjacency info.
        dot_prod = sum(a*b for a,b in zip(base.elems,other.elems))
        len_2_of_diff = base.len_2 + other.len_2 - 2*dot_prod
        if is_useful_metric(len_2_of_diff):
            new_elems = tuple(a-b for a,b in zip(base.elems,other.elems))
            # compares as less if the first non 0 element is negative
            if new_elems < bases_TUPLES[0]:
                # we can use a generator here because Vector converts to a tuple anyway
                # we only needed to convert the other one to a tuple to compare to the first tuple in the array
                new_elems = (-a for a in new_elems)
                new_basis = {**other.basis_map, **{k:-v for k,v in base.basis_map.items()}}
            else:
                new_basis = {**base.basis_map, **{k:-v for k,v in other.basis_map.items()}}
            x = Vector(new_elems, basis_map = new_basis, len_2=len_2_of_diff)
            if x.elems not in SEEN:
                bases.append(x)
                SEEN.add(x.elems)
                print(x.elems, base.basis_map.keys(), other.basis_map.keys(),x.basis_map)
        len_2_of_sum = base.len_2 + other.len_2 + 2*dot_prod
        if is_useful_metric(len_2_of_sum):
            basis_map = {**base.basis_map, **other.basis_map}
            x = Vector((a+b for a,b in zip(base.elems,other.elems)),basis_map,len_2_of_sum)
            if x.elems not in SEEN:
                bases.append(x)
                SEEN.add(x.elems)
                print(x.elems, base.basis_map.keys(), other.basis_map.keys(),x.basis_map)

import collections
base_len2 = bases[0].len_2
x = collections.Counter(v.len_2 for v in bases)
for k in sorted(x.keys()):
    print("{:4d}: {:5d}".format(k//base_len2, x[k]))
