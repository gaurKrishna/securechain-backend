from asyncio import constants
from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit
import math

solver = pywraplp.Solver.CreateSolver('GLOP')

#Have to maintain a dict mapping instance id to its corresponding variable
instance_to_var = {
    "Bharat Biotech": "var1",
    "Serum Institute of India": "var2"
}

data = {
  "goal" : 1000,
  "constraints" : [
    {
      "parameters" : [
        {
          "variable" : "Bharat Biotech",
          "coefficient" : 1,
        }
      ],
      "operator" : "<=",
      "constant" : 500,
    },
  ],
}

goal = data.get("goal", None)
constraints = data.get("constraints", None)

variables = list()

#Creating variables
for key in instance_to_var.keys():
  variable = solver.NumVar(0, goal, instance_to_var[key])
  instance_to_var[key] = variable
  variables.append(variable)


cts = list()


# #Goal Constraint
ct = solver.Constraint(goal, goal, "goal_constraint")
for key in instance_to_var.keys():
  ct.SetCoefficient(instance_to_var[key], 1)
cts.append(ct)


#Creating constraints
i = 0
for constraint in constraints:
  parameters = constraint.get("parameters")
  constant = int(constraint.get("constant"))

  ct = solver.Constraint(0, constant, f"ct{i}")
  for parameter in parameters:
    ct.SetCoefficient(instance_to_var[parameter.get("variable")], parameter.get("coefficient"))
  cts.append(ct)

print(solver.constraints())

objective = solver.Objective()


objective.SetCoefficient(variables[0], 1)
objective.SetCoefficient(variables[1], 2)

objective.SetMinimization()

solver.Solve()
print('Solution:')
print('Objective value =', objective.Value())

for variable in variables:
  print(f'{variable} =', variable.solution_value())
