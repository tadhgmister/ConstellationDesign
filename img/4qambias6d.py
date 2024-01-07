from shapesin6d import visual_bias_vectors_6d
from plotutil import HighDimScatter
import itertools

QAM4points = list(itertools.product([0, 2], repeat=2))

fig = HighDimScatter(6, "4QAM biassed in 6d", range(4))
for bias in visual_bias_vectors_6d:
    fig.scatter([tuple(a+b for a,b in zip(bias,p*3)) for p in QAM4points])

fig.scatter([(2,2.6, 2.1,2.6, 2,2.6)])

fig.save()
