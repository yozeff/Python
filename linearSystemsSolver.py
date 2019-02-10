#Joseph Harrison 2019
from matrixClass import Matrix

def get_variables():
    variables = []
    variable = input('variable: ')
    while variable != 'END':
        variables.append(variable)
        variable = input('variable: ')
    return variables

def get_equations(variables):
    equations = []
    solutions = []
    for i in range(len(variables)):
        print('Eq',i+1,': ')
        equation = []
        for j in range(len(variables)):
            equation.append(float(input('coeff of '+variables[j]+': ')))
        solutions.append(float(input('solution: ')))
        equations.append(equation)
    return equations,solutions

def run():
    variables = get_variables()
    equations,solutions = get_equations(variables)
    solutions = Matrix([[solution] for solution in solutions])
    inverseEqMatrix = Matrix(Matrix(equations).invert())
    values = [item[0] for item in solutions * inverseEqMatrix]
    for pair in [item for item in zip(variables,values)]:
        print(pair[0],'=',pair[1])

answer = 0
while answer != 'END':
    run()
    answer = input('"END" to end: ')
