# first import the Model class from docplex.mp (python calls cplex to solve)
from docplex.mp.model import Model

# create one model instance, with a name
m = Model(name='telephone_production')

# by default, all variables in Docplex have a lower bound of 0 and infinite upper bound
desk = m.continuous_var(name='desk')
cell = m.continuous_var(name='cell')

# write constraints
# constraint #1: desk production is greater than 100
m.add_constraint(desk >= 100, ctname = 'desk_demand')

# constraint #2: cell production is greater than 100
m.add_constraint(cell >= 100, ctname = 'cell_demand')

# constraint #3: assembly time limit
ct_assembly = m.add_constraint( 0.2 * desk + 0.4 * cell <= 400, ctname = 'assembly')

# constraint #4: painting time limit
ct_painting = m.add_constraint( 0.5 * desk + 0.4 * cell <= 490, ctname = 'painting')

m.maximize(12 * desk + 20 * cell)

#step1-print information6
m.print_information()
print("\n")

#step2-solve problem
s = m.solve()

#step3-solution status details
print(m.solve_details)
print("\n")

#step4-print solution
m.print_solution()

