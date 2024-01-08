from plotutil import HighDimScatter
import itertools

visual_bias_vectors_6d = [
    (0,0,0,0,0,0),
    (1,0,1,0,1,1),
    (0,1,1,1,0,1),
    (1,1,0,1,1,0)]
if __name__ == "__main__":

    fig = HighDimScatter(6, "tetrahedrons in 6d", {0:"0", 0.5:"1/2"}, figsize=3)
    for x in visual_bias_vectors_6d:
        fig.scatter([tuple(a/2 for a in x)])

    fig.save()
