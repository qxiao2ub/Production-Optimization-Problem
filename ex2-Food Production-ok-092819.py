#pandas is for using reading functions
import pandas as pd
products = pd.read_csv('products.csv',header=None)
resources = pd.read_csv('resources.csv',header=None)
consumptions = pd.read_csv('consumptions.csv',header=None)


products = products.values.tolist()
resources = resources.values.tolist()
consumptions = consumptions.values.tolist()

print('Here is products information:', products)
print('Here is resources information:', resources)
print('Here is consumptions information:', consumptions)

#python calls cplex
from docplex.mp.model import Model
mdl = Model(name='production')

# define decision variables
# 6 decision variables
inside_p=[]
for i in range(0,len(products)):
    inside_p.append( mdl.continuous_var(name= 'inside_%s' % products[i][0]))

outside_p=[]
for i in range(0,len(products)):
    outside_p.append( mdl.continuous_var(name= 'outside_%s' % products[i][0]))
    
# demand satisfaction
# 3 constraints
for i in range(0,len(products)):
    mdl.add_constraint(inside_p[i]+outside_p[i] >= products[i][1])
    
# resource capacity 
# 2 constraints
for j in range(0,len(resources)):
    mdl.add_constraint(mdl.sum(consumptions[i][j+1]*inside_p[i] for i in range(len(products)))<= resources[j][1])

# objective expressions
# inside cost
mdl.total_inside_cost = mdl.sum(inside_p[i] * products[i][2] for i in range(len(products)))
# outside cost
mdl.total_outside_cost = mdl.sum(outside_p[i] * products[i][3] for i in range(len(products)))
# minimize totoal cost
mdl.minimize(mdl.total_inside_cost + mdl.total_outside_cost)

#step1-print information
mdl.print_information()
print("\n")

#assert mdl
#mdl.display()

from docplex.util.environment import get_environment

if mdl.solve():
    mdl.print_solution()
    # Save the CPLEX solution as "solution.json" program output
    with get_environment().get_output_stream("solution.json") as fp:
        mdl.solution.export(fp, "json")
else:
    print("Problem has no solution")
    
print("---------------")   
#To get all variable values
print("Decision Variable Values are:")
print(mdl.solution.get_all_values())

print("---------------")
#To get objective value
print("Optimal Objective Values is:")
print(mdl.solution.get_objective_value())

