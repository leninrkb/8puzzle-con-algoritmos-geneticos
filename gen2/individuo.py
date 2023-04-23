import numpy as np
class Individuo:
    def __init__(self, genes, binario=None):
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
                indice = self.genes.index(listamodelo[i])
                aux = self.genes[i]
                self.genes[i] = listamodelo[i]
                self.genes[indice] = aux

    def ver_genes(self):
        print(f'*** genes:\n{np.array(self.genes).reshape(3,3)}\nbinario:\n{self.binario}\n')