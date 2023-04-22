import numpy as np

class Individuo:
    def __init__(self):
        self.genes = np.array([
            [2, 3, 6],
            [0, 4, 8],
            [1, 7, 5]
        ])
        self.probabilidad_reproduccion = 0

    def poscicion_cero(self):
        x, y = self.genes.shape
        for i in range(x):
            for j in range(y):
                if self.genes[i, j] == 0:
                    return (i, j)
    def mover_arriba(self):
        x, y = self.poscicion_cero()
        if x-1 >= 0:
            self.genes[x, y], self.genes[x-1, y] = self.genes[x-1, y], self.genes[x, y]
            return True
        return False
    def mover_izquierda(self):
        x, y = self.poscicion_cero()
        if y-1 >= 0:
            self.genes[x, y], self.genes[x, y-1] = self.genes[x, y-1], self.genes[x, y]
            return True
        return False
    def mover_abajo(self):
        x, y = self.poscicion_cero()
        if x+1 <= 2:
            self.genes[x, y], self.genes[x+1, y] = self.genes[x+1, y], self.genes[x, y]
            return True
        return False
    def mover_derecha(self):
        x, y = self.poscicion_cero()
        if y+1 <= 2:
            self.genes[x, y], self.genes[x, y+1] = self.genes[x, y+1], self.genes[x, y]
            return True
        return False
    
    def imprimir_individuo(self):
        print(f'genes:\n {self.genes} \n')