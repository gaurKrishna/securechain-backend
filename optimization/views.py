from ast import operator
from inspect import Parameter
from urllib import response
from rest_framework.views import APIView
from rest_framework import status, permissions, authentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ortools.linear_solver import pywraplp

from supplychain.models import SupplyChain
from entities.models import Entity, Instance


class OptimizationApi(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        supplychain_id = kwargs.get("supplychain", None)
        entity_id = kwargs.get("entity", None)

        if supplychain_id is None or entity_id is None:
            return Response({"Error": "Supply chain id or entity id could not be none"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            supplychain = SupplyChain.objects.get(id = supplychain_id)
        except SupplyChain.DoesNotExist:
            return Response({"Error": "Invalid Supply chain id"}, status = status.HTTP_400_BAD_REQUEST)
        
        try: 
            entity = Entity.objects.get(id = entity_id)
        except Entity.DoesNotExist:
            return Response({"Error": "Invalid entity id"}, status = status.HTTP_400_BAD_REQUEST)
        
        instances = Instance.objects.filter(entity = entity)

        # Dictionary to maintain a mapping from instance id to corresponding variable
        instance_to_var = dict()
        i = 0
        for instance in instances:
            instance_to_var[instance.id] = f"var{i}"
        
        data = request.data

        goal = data.get("goal", None)
        constraints = data.get("constraints", None)

        if goal is None or constraints is None:
            return Response({"error": "Goal or constraints can not be none"}, status=status.HTTP_400_BAD_REQUEST)
        
        goal = int(goal)

        #Creating solver object for optimization problem
        solver = pywraplp.Solver.CreateSolver('GLOP')

        #Creating Variables
        for key in instance_to_var.keys():
            variable = solver.NumVar(0, goal, instance_to_var[key])
            instance_to_var[key] = variable #Assign actual variable to instance id

        #Goal constraint
        ct = solver.Constraint(goal, goal, "goal_constraint")
        for key in instance_to_var.keys():
            ct.SetCoefficient(instance_to_var[key], 1)

        #Creating Constraints
        i = 0
        for constraint in constraints:
            parameters = constraint.get("parameters")
            constant = int(constraint.get("constant"))
            operator = constraint.get("operator")
            start = 0

            if operator == '=':
                start = constant
            
            ct = solver.Constraint(start, constant, f"ct{i}")
            
            for parameter in parameters:
                print(instance_to_var[parameter.get("variable")])
                print(parameter.get("coefficient"))
                coefficient = parameter.get("coefficient", None)
                
                if coefficient is None:
                    return Response({"error": "coefficient can't be none"}, status=status.HTTP_400_BAD_REQUEST)

                coefficient = int(coefficient)
                
                ct.SetCoefficient(instance_to_var[parameter.get("variable")], coefficient)

        objective = solver.Objective()
        
        i = 1 
        for key in instance_to_var.keys():
            objective.SetCoefficient(instance_to_var[key], i)
            i += 1
    
        objective.SetMinimization()
        solver.Solve()

        response_dict = {"objective_value": objective.Value()}

        for key in instance_to_var.keys():
            response_dict[key] = instance_to_var[key].solution_value()

        return Response(
            response_dict,
            status = status.HTTP_200_OK
        )