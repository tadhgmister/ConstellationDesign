"""
has some logic to do combinotorics to generate constellation clouds tracking the bit count and energy etc.
Caches the minimum distance which is calculated by brute force and product/bias is not made intelligently to track distance vectors

"""


import numpy as np
import itertools
import math
import gc
import collections
def QAM(bits_per_dim):
    "returns an array of symbols for a single dimension of QAM"
    q = np.array([0])
    for it in range(bits_per_dim):
        q = np.cat(2*q + 1, 2*q - 1)


#qam16 = QAM(2)

class Constellation:
    _cached_dists = None # will be set to dictionary of (a,b):abs(codeword[a] - codeword[b])
    def __init__(self, points):
        self.codewords = list(points) # cast to list so iterators turn to iterable
        self.dims = self.codewords[0].size
        assert all(a.size==self.dims for a in self.codewords), "all codewords must be same dimensionality"
        # there should probably be a lot more checks here but I'll probably implement them when they become a problem
        self.bits = math.log2(len(self.codewords))

    def _populate_cached_dists(self):
        "calculates the distance between all points in the constellation"
        BASE = np.array(self.codewords)
        print(BASE.shape)
        self._cached_dists = collections.Counter()
        for a in range(len(self.codewords)):
            #print(f"done {a:6d} out of {len(self.codewords)}")
            
            dist_from_a = BASE[a+1:,:] - BASE[a,:]
            norms = np.sum(dist_from_a * dist_from_a, axis=1)
            for b in range(norms.size):
                #assert norms[b] != 0, "codeword {} appears twice".format(self.codewords[a])
                self._cached_dists[float(norms[b])] += 1
            assert self._cached_dists[0] == 0, "repeats found"
                
    def _maybe_pop_dists(self):
        if self._cached_dists is None:
            self._populate_cached_dists()
    def min_d(self):
        "returns min dist between codewords"
        return math.sqrt(self.min_d2())
    def min_d2(self):
        "returns the square of minimum distance between codewords"
        self._maybe_pop_dists()
        return min(self._cached_dists.keys())
    def bits_per_dim(self):
        return self.bits/self.dims
    def energy_per_dim(self):
        "calculates the average energy used per dimension of the constellation"
        return sum(np.inner(a,a) for a in self.codewords)/len(self.codewords)/self.dims
    def ave_n_neighboors(self):
        "returns the average number of neighbours with *exactly* the min distance"
        # multiply min dist by a small factor to account for floating point imprecisions
        # but also if a neighboor is that close to the actual min counting it is fine
        min_d2 = self.min_d2() * 1.000001
        self._maybe_pop_dists()
        prox = sum(c for d,c in self._cached_dists.items() if d<=min_d2)
        # here we only calculated each distance once but in the actual summation we'd need to double count it for both symbols, hence the *2
        return prox*2/len(self.codewords)
    def product(*consts, repeat=1):
        "returns new constellation which is cartesian product of both (as seperate dims)"
        return Constellation(map(np.concatenate, itertools.product(*(val.codewords for val in consts), repeat=repeat)))
    def bias(*consts):
        """
        takes 2 constellations with same dimensionality and returns a new constellation by adding elementwise each code word of each
        is similar to .product but instead of taking constellations of any dimensionality and returning one with higher dimensionality
        this takes all same dimensionality and densifies the grid"""
        return Constellation(map(sum, itertools.product(*(val.codewords for val in consts))))
    def center(self):
        "returns copy of self where the average value is 0"
        c = sum(self.codewords)/len(self.codewords)
        new_const = Constellation(a-c for a in self.codewords)
        # centering doesn't change distances so copy it over if we've already computed it
        new_const._cached_dists = self._cached_dists
        return new_const
    def scale(self, factor):
        "scales every codeword by a constant factor"
        new_const = Constellation(a*factor for a in self.codewords)
        #if self._cached_dists is not None:
        #    new_const._cached_dists = {k:v*factor for k,v in self._cached_dists.items()}
        return new_const

    def summary(self, title=""):
        return f"""
Constellation {title}:
        dimensionality: {self.dims}
        bits/dim:       {self.bits_per_dim()}
        energy/dim:     {self.energy_per_dim()}
        neighb (norm)   {self.ave_n_neighboors()}
        min dist:       {self.min_d()}
"""


    
qpsk = Constellation([np.array([-1]), np.array([+1])])
# since we are doing it per dimension bpsk and qpsk are identical, we aren't doing complex numbers here.
qam16 = qpsk.scale(2).bias(qpsk)

print(qam16.dims, qam16.energy_per_dim(), qam16.bits_per_dim(), qam16.min_d())


AAA = Constellation([np.array([0,0,0,0]),
                     np.array([1,1,1,1])])

BBB = AAA.scale(2).bias(AAA)
CCC = qam16.product(repeat=4).bias(AAA)


assert len(CCC.codewords) == len(set(map(tuple,CCC.codewords))), "Nope :("
print("YEP")



def tetra_pattern(a,b):
    return Constellation([np.array([*a,*a,*a]),
                          np.array([*a,*b,*b]),
                          np.array([*b,*a,*b]),
                          np.array([*b,*b,*a])])
tetra1 = tetra_pattern((0,0), (1,1)).center()
thingy = qpsk.product(repeat=6).bias(tetra1)

def tetra_6():
    for ia in range(6):
        for ib in range(ia+1, 6):
            v = [0,0]*6
            v[2*ia] = v[2*ib] = 1
            v[2*ia+1] = v[2*ib+1] = 1
            yield np.array(v)

tetra2 = Constellation(tetra_6())

print(qpsk.summary("qpsk"))
print(tetra1.summary("tetra 1"))
print(tetra2.summary("tetra 2"))
print(thingy.summary("qpsk + tetra1"))





bestest = tetra1.product(tetra1).bias(tetra2)
print(bestest.summary("tetra1 + tetra2"))
#def d(x):
#    return np.sum(np.mod(bestest.codewords[0] - x, 2))
#print(*map(d, bestest.codewords[1:]), sep="\n")
#print(bestest.codewords[-10])
#raise None
#bigone = bestest.bias(qpsk.product(repeat=12))
#print(bigone.summary())

test = Constellation([np.array([0,0,0,0,0,0,0,0]),
                      #np.array([1,0,1,0,1,0,1,0]),
                      #np.array([0,1,0,1,0,1,0,1]),
                      np.array([1,1,1,1,1,1,1,1])]).center()

newthing = test.product(repeat=3).bias(tetra1.product(repeat=4))
def calc_mod_dist(const):
    def d(x, y=const.codewords[0]):
        return np.sum(np.mod(x-y, 2))
    return min(map(d, const.codewords[1:]))
print(calc_mod_dist(newthing))
#print(newthing.summary())

