from random import shuffle
import random
import numpy  as np
from individuo import Individuo

def alterar_genes(genes):
        flat_gen = genes.flatten().tolist()
        shuffle(flat_gen)
        nuevos_genes = np.array(flat_gen).reshape(genes.shape)
        return nuevos_genes

def generar_poblacion(generar=50):
    poblacion = []
    for i in range(generar):
        individuo_nuevo = Individuo()
        individuo_nuevo.genes = alterar_genes(individuo_nuevo.genes)
        # individuo_nuevo.imprimir_individuo()
        poblacion.append(individuo_nuevo)
    return poblacion

def  generar_rango(rango):
    rango_inicio, rango_fin = rango
    rango_seleccion = []
    for i in range(rango_inicio, rango_fin+1):
          if i%2==0:
               rango_seleccion.append(i)
    # print(rango_seleccion)
    return rango_seleccion

def seleccionar_rango(rango_seleccion):
     posicion_random = random.randint(0, len(rango_seleccion)-1)
     numero_subconjunto = rango_seleccion[posicion_random]
     return numero_subconjunto

def seleccionar_poblacion_inicial(poblacion, rango=(4,8)):
    rango_seleccion = generar_rango(rango)
    numero_subconjunto = seleccionar_rango(rango_seleccion)
    print(numero_subconjunto)
    subconjunto = random.sample(poblacion, numero_subconjunto)
     