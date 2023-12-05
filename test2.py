"""
Has construct to manage constellations with energy, bits, distances
and will store vector distances as a Counter for the whole constellation

seems incomplete or at least untested, Constellation._generate_dists_from_prod has 4 arguments but it is called with 3 from .product

"""

import math
import itertools
import collections

class Dist(tuple):
    """
    a thin wrapper around tuples that allow adding and subtracting element wise
    A caveat is that for our implementation it is highly desirable for a distance and the
    negative distance (negating all elements) to be equivelent, so when distances are subtracted the
    'larger' one by sequence meaning of larger is kept positive, this means essentially that the first
    non 0 element of a distance will be guarenteed to be positive as long as it was constructed by subtracting
    other distances, the initializer doesn't normalize the distance immidiately so that points in a constellation can be cast to Dist
    for convinient math but subtracting them will give this normalization.
    """
    def __add__(self, other):
        # when both are normalized we should always get a normalized one out by adding
        return Dist(a+b for a,b in zip(self,other))
    def __sub__(self, other):
        # for subtraction we want to make sure the "bigger" one is subtracted
        # note that "bigger" means the earliest element that is different is larger (in the tuple sense)
        if tuple.__lt__(self, other):
            it = zip(other, self)
        else:
            it = zip(self, other)
        return Dist(a-b for a,b in it)
    def size(self):
        "returns the sum of square of each element, like abs(x)^2 for vectors"
        return sum(a**2 for a in self)
    @classmethod
    def concat(cls,*elems):
        "concatinates several sequences into single distance"
        return cls(itertools.chain.from_iterable(elems))
    def scale(self, factor):
        return Dist(a*factor for a in self)

class Constellation:
    """
    constellation in digital communications sense, a cloud of points representing code words to transmit messages
    - energy is proportional to average value of square of magnitude of vectors
    - dims is the number of dimensions
    """
    def __init__(self, coordinates_iter, dists, n_points, energy, dims, min_dist):
        self._points = coordinates_iter #we will keep this around but not actually use it ever
        self.dists = dists
        self.n_points = n_points
        self.energy = energy
        self.dims = dims
        self.min_dist = min_dist

    @classmethod
    def from_cloud(cls, points):
        """initializes a new constellation from a given set of points
        (the constructor takes a lot of stuff that is calculated internally when composing multiple constellations)
        """
        points = list(map(Dist,points)) # note we are relying on the normalization not happening at this stage which is a little jank
        assert len(points) > 1, "a constellation should have at least 2 points in it"
        assert hasattr(points[0], "__len__"), "constellation needs to be sequences of coordinates"
        dims = len(points[0])
        total_dist = Dist((0,)*dims)
        tot_energy = 0
        for p in points:
            assert len(p)==dims, "not all points have same dimensionality"
            tot_energy += p.size()/len(points) 
        print("tot_energy before", tot_energy)
        # I'm not going to care about shifting all the points to center them, most cases it is easier to reason
        # about when we specifically don't do that, but it is assumed that we'll not waste the power for constant shift in a direction
        tot_energy -= Dist.size(sum(x)/len(points) for x in zip(*points))
        print("after: ", tot_energy)
        dists,min_dist = cls._generate_dists_from_points(points)
        return cls(points, dists, len(points), tot_energy, dims, min_dist)
        

    @staticmethod
    def _generate_dists_from_points(points):
        """
        takes iterable of points and brute force figures out the minimum distance between neighbours and generates
        a Counter with the distances between points and corresponding 
        """
        dists = collections.Counter()
        min_dist2 = float("inf")
        for i,p in enumerate(points):
            for p2 in points[i+1:]:
                d = p-p2
                if d.size() < min_dist2:
                    # new minimum distance, all previous neighboors are not nearest
                    dists.clear()
                    min_dist2 = d.size()
                dists[d] += 1

        return dists, math.sqrt(min_dist2)
            
    @property
    def energy_per_dim(self):
        return self.energy/self.dims
    @property
    def bits_per_dim(self):
        return math.log2(self.n_points)/self.dims
    @property
    def ave_neighbours(self):
        return 2*sum(self.dists.values())/self.n_points

    def summary(self,name=""):
        return f"""constellation {name}: (min dist = {self.min_dist})
        dimensionality: {self.dims}
        energy/dim:     {self.energy_per_dim}
        bits/dim:       {self.bits_per_dim}
        #neighbours:    {self.ave_neighbours}
        neighbours norm:{self.ave_neighbours/self.dims}
        cardinality:    {len(self.dists.keys())}"""
    

    def read_points(self):
        """
        returns the coordinate iterator, IMPORTANT: this is only guarenteed to work once for a constellation that
        was composed from other constellations and by iterating through it all intermediate constellations have their
        iterator exhausted so are also not usable.
        this is because the cloud of points is never used internally at all but with iterators it is very cheap to maintain a single
        use sequence to enumerate all points in the constellation so we do that, but buy and large you shouldn't rely on this more
        than once per tree of constellations composed from direct ones.
        """
        return self._points

    def scale(self, factor):
        """
        returns a constellation formed by scaling the AMPLITUDE by factor (so the power gets scaled by factor**2
        """
        def mul_by_factor(p,f=factor):
            return type(p)(a*f for a in p)
        return Constellation(map(mul_by_factor, self._points),
                             dists=collections.Counter((d.scale(factor), count) for d,count in self.dists.items()),
                             n_points=self.n_points,
                             energy = self.energy * factor**2,
                             dims = self.dims,
                             min_dist = self.min_dist * factor)

    def product(*consts, repeat=1):
        """
        computes cartesian product of several constellations (very similar to itertools.product)
        this will increase the dimensionality by the sum of all constellations or if you just do x.product(repeat=4)
        it will multiply the dimensionality by 4 etc.
        """
        points = map(Dist.concat, itertools.product(*(x._points for x in consts), repeat=repeat))
        n_points = 1
        energy = 0
        dims = 0
        for c in consts:
            n_points *= c.n_points
            energy += c.energy
            dims += c.dims
        n_points **=repeat
        energy *= repeat
        dims *= repeat
        dist_prod = consts[0]._generate_dists_from_prod(consts,repeat,n_points)
        return Constellation(coordinates_iter = points,
                             dists=dist_prod,
                             n_points=n_points,
                             energy = energy,
                             dims = dims,
                             min_dist = min(c.min_dist for c in consts))
                             
    @staticmethod
    def _generate_dists_from_prod(consts, repeat, n_points_total, dims_total):
        dists = collections.Counter()
        consts = consts*repeat #this should just do sequence repetition, not worth optimizing for repeat somehow
        dims_before = 0
        for constellation in consts:
            count_reps = n_points_total / constellation.n_points #number of points orthagonal to this constellation for which all the # of vectors will be multiplied
            padding_before = (0,)*dims_before
            padding_after = (0,)*(dims_total-dims_before-constellation.dims)
            for part_d_vec, count in constellation.dists.items():
                new_d_vec = Dist((*padding_before, *part_d_vec, *padding_after))
                dists[new_d_vec] = count*count_reps
                # don't need += here because it can't possibly get the same from another constellation in this function
        return dists

    def bias(*consts,suppress_warning_of_lower_min_dist=False):
        """
        returns a new constellation made by adding several constellations of equal dimensionality elementwise
        """
        points = map(sum, itertools.product(*(x._points for x in consts), repeat=repeat))
        n_points = 1
        energy = 0
        dims = consts[0].dims
        for c in consts:
            assert c.dims == dims, "can only call bias on constellations of equal dimensionality"
            n_points *= c.n_points
            energy += c.energy
        dist_prod, new_min_dist = consts[0]._generate_dists_from_bias(consts,n_points,suppress_waning_of_lower_min_dist)
        return Constellation(coordinates_iter = points,
                             dists=dist_prod,
                             n_points=n_points,
                             energy = energy,
                             dims = dims,
                             min_dist = new_min_dist)
    @staticmethod
    def _generate_dists_from_bias(A, B, silent):
        "A and B are tuples of (dists, min_dist, n_points)"
        new_dists = collections.Counter()
        [dists1, min_dist1, n_points1] = A
        [dists2, min_dist2, n_points2] = B
        for d,c in dists1.
        
        

basic = Constellation.from_cloud([[0], [2]])
t2 = basic.scale(2)

print(basic.summary("t2"))
