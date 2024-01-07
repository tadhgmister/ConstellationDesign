from shapesin6d import visual_bias_vectors_6d
from plotutil import HighDimScatter
import itertools

QAM16points = list(itertools.product([0, 2, 4, 6], repeat=2))

fig = HighDimScatter(6, "16QAM biassed in 6d", range(8))
for bias in visual_bias_vectors_6d:
    fig.scatter([tuple(a+b for a,b in zip(bias,p*3)) for p in QAM16points])

fig.save()
