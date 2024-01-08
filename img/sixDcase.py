from shapesin6d import visual_bias_vectors_6d
from plotutil import HighDimScatter
import itertools

QAM4points = list(itertools.product([0, 1], repeat=2))

fig = HighDimScatter(6, "4QAM biassed in 6d", {i/2:f"{i}/2" for i in range(4)})
for bias in visual_bias_vectors_6d:
    fig.scatter([tuple(a/2+b for a,b in zip(bias,p*3)) for p in QAM4points])

if __name__ == "__main__":
    fig.save()
