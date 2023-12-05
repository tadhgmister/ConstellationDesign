import itertools
bias_A = (1,1,1,1,0,0)
bias_B = (1,1,0,0,1,1)

ALL_BIASSES = [(0,0,0,0,0,0), bias_A, bias_B, tuple(x^y for x,y in zip(bias_A,bias_B))]

all_points = set()
for q1 in [0,2]:
 for q2 in [0,2]:
  for q3 in [0,2]:
   for q4 in [0,2]:
    for q5 in [0,2]:
     for q6 in [0,2]:
      QAM_point = (q1,q2,q3,q4,q5,q6)
      for bias_vector in ALL_BIASSES:
          point = tuple(x+y for x,y in zip(QAM_point, bias_vector))
          for other in all_points:
              if sum((t1-t2)**2 for t1,t2 in zip(point,other)) < 2:
                  raise Exception("{} and {} are less than 2 units apart".format(point,other))
          all_points.add(point)
          print(point,end=", ")
      print() # newline at each QAM point
