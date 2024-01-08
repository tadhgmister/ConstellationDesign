import itertools
from plotutil import HighDimScatter
# Create meshgrid using itertools.product
QAM16points = list(itertools.product([0, 1], repeat=4))

fig = HighDimScatter(4, "4D 2-pam / 4QAM with bias", {i/2:f"{i}/2" for i in range(4)})
def add_one_to_each(point):
    return tuple(x+1/2 for x in point)
fig.scatter(QAM16points)
fig.scatter(list(map(add_one_to_each, QAM16points)))

fig.save()
