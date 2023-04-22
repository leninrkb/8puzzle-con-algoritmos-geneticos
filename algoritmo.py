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
    print(f'*** poblacion total de individuos generada: {len(poblacion)}')
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
    print(f'*** numero de subconjunto a seleccionar: {numero_subconjunto[0]}')
    subconjunto = random.sample(poblacion, numero_subconjunto[0])
    print(f'*** subconjunto seleccionado: {len(subconjunto)}')
    return subconjunto

def calcular_heuristica(femenino, pretendiente):
    lista_femenino = femenino.genes.flatten().tolist()
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
        total_puntuaciones += puntuacion
        puntuaciones.append((pretendiente, puntuacion))
    # print(puntuaciones)
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
    femenino = poblacion_inicial[poscicion_femenino] 
    print(f'femenino en poscicion: {poscicion_femenino}')
    print(f'femenino : {femenino.genes}')
    # print(f'poblacion_inicial con femenino: {len(poblacion_inicial)}')
    pretendientes = np.delete(poblacion_inicial, poscicion_femenino)
    pretendientes_puntuados = puntuar_pretendientes(femenino, pretendientes)
    print(f'pretendientes len: {len(pretendientes)}')
    masculino = seleccionar_masculino(pretendientes_puntuados)
    print(f'masculino seleccionado:\n {masculino.genes}')
    for i, p in enumerate(pretendientes):
        if np.array_equal(p.genes,masculino.genes):
            pretendientes = np.delete(pretendientes, i)
    print(f'pretendientes len: {len(pretendientes)}')
    resultado = [[femenino, masculino], pretendientes]
    return resultado
    # print(f'poblacion_inicial sin femenino: {len(poblacion_inicial)}')
     