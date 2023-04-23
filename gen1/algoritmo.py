from random import shuffle
import random
import numpy  as np
from gen1.individuo import Individuo
import copy

global PRETENDIENTE_MODELO
PRETENDIENTE_MODELO =  np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])

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
    # print(f'*** poblacion total de individuos generada: {len(poblacion)}')
    return poblacion

def  generar_rango(rango):
    rango_inicio, rango_fin = rango
    rango_seleccion = []
    for i in range(rango_inicio, rango_fin+1):
          if i%2==0:
               rango_seleccion.append(i)
    # print(rango_seleccion)
    return rango_seleccion

# def seleccionar_rango(rango_seleccion):
#      posicion_random = random.randint(0, len(rango_seleccion)-1)
#      numero_subconjunto = rango_seleccion[posicion_random]
#      print(f'*** numero de subconjunto a seleccionar: {numero_subconjunto}\n')
#      return numero_subconjunto

def seleccionar_poblacion_inicial(poblacion, rango=(4,8)):
    rango_seleccion = generar_rango(rango)
    numero_subconjunto = random.sample(rango_seleccion, 1)
    # print(f'*** numero de subconjunto a seleccionar: {numero_subconjunto[0]}')
    subconjunto = random.sample(poblacion, numero_subconjunto[0])
    # print(f'*** subconjunto seleccionado: {len(subconjunto)}')
    return subconjunto

def calcular_heuristica(femenino, pretendiente):
    lista_femenino = PRETENDIENTE_MODELO.flatten().tolist()
    lista_masculino = pretendiente.genes.flatten().tolist()
    heuristica = 0
    for index in range(len(lista_femenino)):
        if not lista_femenino[index] == lista_masculino[index]:
            heuristica+=1
    return heuristica

def puntuar_pretendientes(femenino, pretendientes):
    puntuaciones = []
    total_puntuaciones = 0
    for pretendiente in pretendientes:
        heuristica = calcular_heuristica(femenino, pretendiente)
        puntuacion =  9 - heuristica
        if puntuacion >= 5:
            print(f'buena puntuacion:{puntuacion}')
            # input('continuar: ')
        if puntuacion >= 6:
            print(f'solucion encontrada!!!!! \n{pretendiente.genes}')
            input('continuar: ')

        total_puntuaciones += puntuacion
        puntuaciones.append((pretendiente, puntuacion))
    # print(f'puntuaciones totales: {total_puntuaciones}')
    if total_puntuaciones == 0:
        puntuaciones = []
        for pretendiente in pretendientes:
            puntuacion = 1
            total_puntuaciones += puntuacion
            puntuaciones.append((pretendiente, puntuacion))
    probabilidad_aparicion = []
    for pretendiente in puntuaciones:
        probabilidad = int(round(pretendiente[1]/total_puntuaciones, 2) * 100)
        probabilidad_aparicion.append([pretendiente[0], probabilidad])
        # probabilidad_aparicion.append([' ', probabilidad])
    probabilidad_aparicion = sorted(probabilidad_aparicion, key=lambda item : item[1], reverse=True)
    # print(probabilidad_aparicion)
    suma = 0 
    for i in probabilidad_aparicion:
        suma += i[1]
    suma = int(suma)
    # print(f'\n{suma}\n')

    if suma > 100:
        r = suma - 100
        probabilidad_aparicion[-1][1] = probabilidad_aparicion[-1][1] - r
    elif suma < 100:
        r = 100 - suma
        probabilidad_aparicion[0][1] = probabilidad_aparicion[0][1] + r

    suma = 0 
    for i in probabilidad_aparicion:
        suma += i[1]
    suma = int(suma)
    # print(f'\n{suma}\n')
    # print(probabilidad_aparicion)

    return probabilidad_aparicion

def seleccionar_masculino(pretendientes_puntuados):
    ruleta = [i for i in range(100)]
    indices_tomados = []
    for pretendiente in pretendientes_puntuados:
        apariciones = pretendiente[1]
        contador = 0
        while contador <= apariciones:
            if len(indices_tomados) == 100:
                break
            indice = random.randint(0,99)  
            if indice not in indices_tomados:
                ruleta[indice] = pretendiente[0]
                indices_tomados.append(indice)
                contador+=1
    indice_masculino = random.randint(0, 99)
    masculino = ruleta[indice_masculino]
    return masculino
            
def seleccionar_padres(poblacion_inicial):
    poscicion_femenino = np.random.choice(len(poblacion_inicial))
    # print(f'pos: {poscicion_femenino}')
    femenino = poblacion_inicial[poscicion_femenino] 
    # print(f'femenino en poscicion: {poscicion_femenino}')
    # print(f'femenino : {femenino.genes}')
    # print(f'poblacion_inicial con femenino: {len(poblacion_inicial)}')
    pretendientes = np.delete(poblacion_inicial, poscicion_femenino)
    pretendientes_puntuados = puntuar_pretendientes(femenino, pretendientes)
    # print(f'pretendientes len: {len(pretendientes)}')
    masculino = seleccionar_masculino(pretendientes_puntuados)
    # print(f'masculino seleccionado:\n {masculino.genes}')
    for i, p in enumerate(pretendientes):
        # print(f'index: {i}, pretendientes:{len(pretendientes)}')
        if np.array_equal(p.genes,masculino.genes):
            pretendientes = np.delete(pretendientes, i)
            break
    # print(f'pretendientes len: {len(pretendientes)}')
    resultado = [[femenino, masculino], pretendientes]
    return resultado
    # print(f'poblacion_inicial sin femenino: {len(poblacion_inicial)}')


def cruce(femenino, masculino):
    lista_f = femenino.genes.flatten().tolist()
    lista_m = masculino.genes.flatten().tolist()
    # print(f'lista f:\n {lista_f}\nlista m:\n {lista_m}\n')

    indices_f = [(indice, valor) for indice, valor in enumerate(lista_f)]
    indices_m = [(indice, valor) for indice, valor in enumerate(lista_m)]
    # print(f'lista indices f:\n {indices_f}\nlista indices m:\n {indices_m}\n')

    indices_f_ord = sorted(indices_f, key=lambda val : val[1])
    indices_m_ord = sorted(indices_m, key=lambda val : val[1])
    # print(f'lista indices ord f:\n {indices_f_ord}\nlista indices ord m:\n {indices_m_ord}\n')

    punto_corte = random.randint(1,7)
    # print(f'corte en: {punto_corte}')

    corte1_f = indices_f_ord[:punto_corte]
    corte2_f = indices_f_ord[punto_corte:]
    # print(f'corte femenino. \np1:{corte1_f}\np2:{corte2_f}\n')

    corte1_m = indices_m_ord[:punto_corte]
    corte2_m = indices_m_ord[punto_corte:]
    # print(f'corte masculino. \np1:{corte1_m}\np2:{corte2_m}\n')

    genes1 = corte1_f + corte2_m
    genes2 = corte2_f + corte1_m

    genes1 = sorted(genes1, key=lambda val: val[0])
    genes2 = sorted(genes2, key=lambda val: val[0])

    genes1 = [i[1] for i in genes1]
    genes2 = [i[1] for i in genes2]

    individuo1 = Individuo()
    nuevos_genes1 = np.array(genes1).reshape(individuo1.genes.shape)
    individuo1.genes = nuevos_genes1
    # individuo1.imprimir_individuo()

    individuo2 = Individuo()
    nuevos_genes2 = np.array(genes2).reshape(individuo2.genes.shape)
    individuo2.genes = nuevos_genes2
    # individuo2.imprimir_individuo()

    return [individuo1, individuo2] 
    # print(f'hijo1:\n{genes1}\nhijo2:\n{genes2}\n')

def mutar(hijos):
    quien_muta = random.randint(0,1)
    hijomutar = hijos[quien_muta]
    hijos[quien_muta] = mutar_genes(hijomutar)
    return np.array(hijos)

def mutar_genes(hijo):
    if hijo.mover_arriba():
        return hijo
    if hijo.mover_abajo():
        return hijo
    if hijo.mover_izquierda():
        return hijo
    if hijo.mover_derecha():
        return hijo


def es_solucion(individuos):
    for ind in individuos:
        if np.array_equal(ind.genes, PRETENDIENTE_MODELO):
            print(ind.imprimir_individuo())
            return True
