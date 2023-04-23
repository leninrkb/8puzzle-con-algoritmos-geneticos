import gen1.algoritmo as al
import numpy as np
import time

poblacion = al.generar_poblacion(20)
poblacion_inical = al.seleccionar_poblacion_inicial(poblacion,(4,10))

contador = 0 
while True:
    al.es_solucion(poblacion_inical)
    padres, poblacion_restante = al.seleccionar_padres(poblacion_inical)
    # time.sleep(2)
    al.es_solucion(padres)
    al.es_solucion(poblacion_restante)
    hijos = al.cruce(padres[0], padres[1])
    al.es_solucion(hijos)
    hijos = al.mutar(hijos)
    al.es_solucion(hijos)
    for h in hijos:
        poblacion_restante = np.append(poblacion_restante, h)
    poblacion_inical = poblacion_restante
    contador+=1
    print(contador)