#Orienteering Problem tidak semua tempat wisata harus dikunjungi
#Importing the package numpy as np.
import numpy as np
# "rnd" is an object that generate random numbers.
rnd = np.random
#"seed(0)" is a method that reset (every time), the same random set of numbers.
rnd.seed(1)
# Number of customers.
n = 10
#The set of nodes without the depot.
N = [i for i in range(1,n+1)]
# The set of nodes + the depot.
V = [0]+ N
# The rating of each node.
# Rating dikali 10 dari nilai sebenarnya
p = np.array([0, 45, 46, 46, 43, 47, 45, 45, 45, 47, 45])
# Coordinates
coordinates = {
    0: (5,5),      # Depot
    1: (8, 20),    # Node 1
    2: (13, 17),   # Node 2
    3: (18, 15),   # Node 3
    4: (14, 6),    # Node 4
    5: (12, 9),    # Node 5
    6: (12,3),     # Node 6
    7: (6,2),      # Node 7
    8: (4,8),      # Node 8
    9: (2,10),     # Node 9
    10: (3,12),    # Node 10
}
# Extract x and y coordinates
loc_x = np.array([coordinates[i][0] for i in sorted(coordinates)])
loc_y = np.array([coordinates[i][1] for i in sorted(coordinates)])
#Importing the package matplotlib.pyplot as plt.
import matplotlib.pyplot as plt
#Plotting the n nodes without the node 0 (depot) and chose the color blue for each node.
plt.scatter(loc_x[1:],loc_y[1:],c='b')
# Associating and plotting each demand in the right of each blue node (customer).
for i in N:
  plt.annotate('$p_{%d}=%d$'%(i,p[i]),(loc_x[i]+0.1,loc_y[i]))
#Ploting the node 0, chosing the red like its color and the square form like a marker.
plt.plot(loc_x[0],loc_y[0],c='r',marker='s')
#Showing the Initial plot.
plt.show()
#Intializing the set of arcs A.
A = [(i,j) for i in V for j in V if i!=j]
#The distance between each node.
t = np.array([
    [float('inf'), 5.4, 14.7, 10.4, 12.5, 14, 14.1, 17.5, 12.6, 6.9],  # From node 1 to others
    [5.4, float('inf'), 10.1, 5.6, 15.3, 12.3, 9.5, 12.7, 10.8, 2.3],  # From node 2
    [14.7, 10.1, float('inf'), 7.8, 9.7, 13.6, 5.8, 6.9, 11.7, 7.8],   # From node 3
    [10.4, 5.6, 7.8, float('inf'), 9.3, 13.5, 4.1, 7.1, 12.4, 3.5],    # From node 4
    [12.5, 15.3, 9.7, 9.3, float('inf'), 4.3, 8.5, 6.4, 2.8, 13.1],    # From node 5
    [14, 12.3, 13.6, 13.5, 4.3, float('inf'), 12.8, 10.6, 1.5, 17.3],  # From node 6
    [14.1, 9.5, 5.8, 4.1, 8.5, 12.8, float('inf'), 6.1, 11.3, 7.2],    # From node 7
    [17.5, 12.7, 6.9, 7.1, 6.4, 10.6, 6.1, float('inf'), 9.1, 10.5],   # From node 8
    [12.6, 10.8, 11.7, 12.4, 2.8, 1.5, 11.3, 9.1, float('inf'), 10.7], # From node 9
    [6.9, 2.3, 7.8, 3.5, 13.1, 17.3, 7.2, 10.5, 10.7, float('inf')],   # From node 10
])
harga = np.array([0, 30000,40000,20000,20000,65000,20000,10000,44000,20000,15000])

#Importing the docplex.mp.model from the CPLEX as Model
from docplex.mp.model import Model
mdl = Model('OP')
#Initializing our binary variable x_i,j
x=mdl.binary_var_dict(A,name='x')
#Initializing our cumulative rating u
u=mdl.integer_var_dict(N,ub=n,name='u') #N himpunan tempat wisata, ub=batas atas u,
#objective function
mdl.maximize(mdl.sum(p[i]*x[i,j] for i, j in A )) #A=himpunan sisi
#first constraint
mdl.add_constraint(mdl.sum(x[0,j] for j in N)==1) #Yg keluar dr depot nilainya harus 1
#second constraint
mdl.add_constraint(mdl.sum(x[i,0] for i in N)==1) #Yg masuk ke depot nilainya harus 1
#third constraint
mdl.add_constraints(mdl.sum(x[i,k] for k in V if k!=i) - mdl.sum(x[k,i] for k in V if k!=i) == 0 for i in N)
#fourth constraint
mdl.add_constraints(mdl.sum(x[k,j] for k in N if k!=j)<=1 for j in V)
#fifth constraint
B_max=200000
mdl.add_constraint(mdl.sum(harga[i]*x[i,j] for i, j in A) <= B_max)
#sixth constraint
mdl.add_constraints(u[i]>=1 for i in N) #karna di python mulai dr 0 jd >=1
#seventh constraint
mdl.add_indicator_constraints_(mdl.indicator_constraint(x[i,j],u[i]-u[j]<=-1)for i,j in A if i!=0 and j!=0)


#Getting the solution
solution = mdl.solve(log_output=True)
#Printing the solution
print(solution)
#Identifing the active arcs.
if solution:
  active_arcs = [a for a in A if x[a].solution_value > 0.9]
  plt.scatter(loc_x[1:],loc_y[1:],c='b')
  for i in N:
    plt.annotate('$p_{%d}=%d$'%(i,p[i]),(loc_x[i]+0.1,loc_y[i]))
  for i,j in active_arcs :
    #Coloring the active arcs
    plt.plot([loc_x[i],loc_x[j]],[loc_y[i],loc_y[j]],c='g',alpha=0.3)
    plt.plot(loc_x[0],loc_y[0],c='r',marker='s')
  #Plotting the solution
  plt.show()
else:
  print("Model did not solve successfully.")
