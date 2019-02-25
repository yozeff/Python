#Joseph Harrison 2019
import tkinter as tk
from matrixClass import *

def process_equation(equation):
    terms = ['']
    i = 0
    for char in equation:
        if char in ['+','-']:
            terms.append('')
            i += 1
            if char == '-':
                terms[i] += char
        else:
            terms[i] += char
    return terms

def get_coeffs():
    equationsText = equations.get('1.0','end').split(',')
    solutionVector = Matrix([[]])
    variables = []
    coeffMatrix = []
    if len(equationsText[:-1]) != len(process_equation(equationsText[:-1][0][:equationsText[:-1][0].find('=')])):
        solutions.delete('1.0','end')
        solutions.insert('end','Insufficient number of equations')
    else:
        for equation in equationsText[:-1]:
            coeffMatrix.append([])
            equation = equation.replace('\n','').replace(' ','')
            solution = float(equation[equation.find('=')+1:])
            solutionVector.matrix[0].append(float(equation[equation.find('=')+1:]))
            terms = [item for item in process_equation(equation[:equation.find('=')]) if item != '']
            for term in terms:
                if term[-1] not in variables:
                    variables.append(term[-1])
                coeffMatrix[-1].append(float(term[:-1]))
        coeffMatrix = Matrix(coeffMatrix).invert()
        if coeffMatrix == 'not invertible':
            solutions.delete('1.0','end')
            solutions.insert('end','No solutions')
        else:
            variableVector = coeffMatrix * solutionVector
            text = ''
            for i in range(len(variables)):
                text += str(variables[i]) + ' = ' + str(variableVector.matrix[0][i]) + '\n'
            solutions.delete('1.0','end')
            solutions.insert('end',text)

root = tk.Tk()
root.title('Linear System Solver')

title = tk.Label(root,text='Linear Systems Solver',font='helvetica 30 bold italic')
title.grid(row=0,column=0,pady=10)

equationsTitle = tk.Label(root,text='Equations',font='helvetica 20 bold')
equationsTitle.grid(row=1,column=0)
equations = tk.Text(root,font='helvetica 20',width=25)
equations.grid(row=2,column=0,padx=20)

solutionsTitle = tk.Label(root,text='Solutions',font='helvetica 20 bold')
solutionsTitle.grid(row=1,column=2)
solutions = tk.Text(root,font='helvetica 20',width=25)
solutions.grid(row=2,column=2,padx=20)

signature = tk.Label(root,text='Joseph Harrison 2019',font='helvetica 18 italic')
signature.grid(row=3,column=2)

evaluateButton = tk.Button(root,text='Evaluate',command=get_coeffs)
evaluateButton.grid(row=2,column=1)

root.mainloop()
