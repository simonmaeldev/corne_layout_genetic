from pymoo.visualization.scatter import Scatter
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import numpy as np

from MySampling import MySampling
from MyCrossover import MyCrossover
from MyMutation import MyMutation
from MyDuplicateElimination import MyDuplicateElimination
from MyProblem import MyProblem


algorithm = NSGA2(pop_size=11,
                  sampling=MySampling(),
                  crossover=MyCrossover(),
                  mutation=MyMutation(),
                  eliminate_duplicates=MyDuplicateElimination())

res = minimize(MyProblem(),
               algorithm,
               ('n_gen', 10),
               seed=1,
               verbose=True)

#Scatter().add(res.F).show()


print("Best solution found: \nX = \n%s\nF = %s" % (res.X[0][0], res.F))

#results = res.X[np.argsort(res.F[:, 0])]
#count = [np.sum([e == "a" for e in r]) for r in results[:, 0]]
#print(np.column_stack([results, count]))

