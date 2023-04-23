import numpy as np
class Individuo:
    def __init__(self, genes:list, binario:list):
        self.genes = genes
        self.binario = binario
        self.puntuacion = None
        self.probabilidad = None

    def puntuar(self):
        self.puntuacion = self.binario.count(1)
        if self.puntuacion == 0:
            self.puntuacion = 1

    def ajusar_con_bin(self, modelo):
        listamodelo = np.array(modelo).flatten().tolist()
        for i in range(len(listamodelo)):
            if self.binario[i] == 1:
                self.genes[i] = listamodelo[i]

    def ver_genes(self):
        print(f'*** genes:\n{self.genes}\nbinario:\n{self.binario}\n')