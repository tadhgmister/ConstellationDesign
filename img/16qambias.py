import itertools
from plotutil import HighDimScatter
# Create meshgrid using itertools.product
QAM16points = list(itertools.product([0, 2, 4, 6], repeat=4))

fig = HighDimScatter(4, "16QAM with bias", range(8))
def add_one_to_each(point):
    return tuple(x+1 for x in point)
fig.scatter(QAM16points)
fig.scatter(list(map(add_one_to_each, QAM16points)))

fig.save()
