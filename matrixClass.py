#Joseph Harrison 2019

class Matrix:

    def __init__(self,matrix):
        self.matrix = matrix

    def __repr__(self): return 'Matrix ' + repr(self.matrix)

    @staticmethod
    def scalar_transform(transform,matrix):
        if str(type(matrix)) != "<type 'list'>":
            return transform(matrix)
        else:
            return [Matrix.scalar_transform(transform,elem) for elem in matrix]

    @staticmethod
    def identity(size): return [[1 if i == j else 0 for i in range(size)] for j in range(size)]

    def __neg__(self): return Matrix(self.scalar_transform(lambda x: -x,matrix))

    def __add__(self,other):
        result = [[0 for i in range(len(self.matrix[0]))] for j in range(len(self.matrix))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                result[i][j] = self.matrix[i][j] + other.matrix[i][j]
        return result

    def __mul__(self,other):
        result = [[0 for i in range(len(other.matrix))] for j in range(len(self.matrix[0]))]
        for i in range(len(self.matrix[0])):
            for j in range(len(other.matrix)):
                sum = 0
                for k in range(len(self.matrix)):
                    sum += self.matrix[k][i] * other.matrix[j][k]
                result[j][i] = sum
        return result

    def __abs__(self):
        if len(self.matrix) != len(self.matrix[0]):
            return 'not square'
        elif len(self.matrix) == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[1][0] * self.matrix[0][1]
        else:
            result = 0
            for i in range(len(self.matrix)):
                range(1,len(self.matrix[0]))
                minor = [[self.matrix[k][j] for j in range(1,len(self.matrix[0]))] for k in range(len(self.matrix)) if k != i]
                if i % 2 == 0:
                    result += self.matrix[i][0] * abs(Matrix(minor))
                else:
                    result += self.matrix[i][0] * abs(Matrix(minor)) * -1
            return result

    def cofactor(self):
        if len(self.matrix) != len(self.matrix[0]):
            return 'not square'
        elif len(self.matrix) == 2:
            return [[self.matrix[1][1],-self.matrix[0][1]],[-self.matrix[1][0],self.matrix[0][0]]]
        else:
            result = [[0 for i in range(len(self.matrix[0]))] for j in range(len(self.matrix))]
            for i in range(len(self.matrix[0])):
                for j in range(len(self.matrix)):
                    result[i][j] = abs(Matrix([[self.matrix[k][l] for l in range(len(self.matrix[0])) if l != j] for k in range(len(self.matrix)) if k != i]))
                    if (i + j) % 2 != 0:
                        result[i][j] *= -1
        return result

    def adjugate(self):
        cofactorMatrix = self.cofactor()
        if len(cofactorMatrix) > 2:
            for i in range(len(cofactorMatrix)):
                for j in range(i):
                    temp = cofactorMatrix[i][j]
                    cofactorMatrix[i][j] = cofactorMatrix[j][i]
                    cofactorMatrix[j][i] = temp
        return cofactorMatrix

    def invert(self):
        try:
            result = self.scalar_transform(lambda x: float(x) / abs(self),self.adjugate())
            return result
        except ZeroDivisionError:
            return 'not invertible'
