from individuo import Individuo
import random as rn
import numpy as np
global MODELO 
MODELO = [
    [1,2,3],
    [4,5,6],
    [7,8,0],
]

def calcular_binario(genes:list):
    lista_modelo = np.array(MODELO).flatten().tolist()
    binario = []
    for i in range(len(genes)):
        if genes[i] == lista_modelo[i]:
            binario.append(1)
        else:
            binario.append(0)
    return binario


def generar_poblacion(semilla:Individuo, densidad:int):
    poblacion = []
    for i in range(densidad):
        nuevos_genes = semilla.genes[:]
        rn.shuffle(nuevos_genes)
        binario = calcular_binario(nuevos_genes)
        nuevo_individuo = Individuo(genes=nuevos_genes, binario=binario)
        nuevo_individuo.puntuar()
        # print(nuevo_individuo.ver_genes())
        poblacion.append(nuevo_individuo)
    return poblacion

def  generar_rango(rango):
    rango_inicio, rango_fin = rango
    rango_seleccion = []
    for i in range(rango_inicio, rango_fin+1):
          if i%2==0:
               rango_seleccion.append(i)
    return rango_seleccion

def seleccionar_poblacion_inicial(poblacion:list, rango=(4,8)):
    rango_seleccion = generar_rango(rango)
    numero_subconjunto = rn.randint(0, len(rango_seleccion)-1)
    subconjunto = rn.sample(poblacion, rango_seleccion[numero_subconjunto])
    return subconjunto


def calcular_probabilidad_seleccion(poblacion:list):
    #calculo total de puntos para tomarlo como mi 100%
    total_puntos = 0
    calculados = []
    for ind in poblacion:
        # ind.puntuar()
        total_puntos += ind.puntuacion
    #divido la puntuacion de cada uno para el total y la redondedo para 
    #saber su porcentaje de aparicion en la ruleta
    total_ruleta = 0
    for ind in poblacion:
        ind.probabilidad = int(round(ind.puntuacion / total_puntos, 2) * 100)
        total_ruleta += ind.probabilidad
        calculados.append(ind)
    # print(total_ruleta)
    
    # orderno a los individuos por su probabilidad de aparicion
    # solo para controlar el 100 de la ruleta
    calculados = sorted(calculados, key=lambda val : val.probabilidad, reverse=True)
    #compruebo que den 100 exactos 
    if total_ruleta > 100:
        r = total_ruleta - 100
        calculados[0].probabilidad = calculados[0].probabilidad - r
    elif total_ruleta < 100:
        r = 100 - total_ruleta
        calculados[-1].probabilidad = calculados[-1].probabilidad + r
    total_ruleta = 0
    for ind in calculados:
        total_ruleta+=ind.probabilidad
    # print(total_ruleta)
    return calculados

def seleccionar_masculino(poblacion):
    ruleta = [0 for i in range(100)]
    indices_tomados = []
    for pretendiente in poblacion:
        apariciones = pretendiente.probabilidad
        contador = 0
        while contador <= apariciones:
            if len(indices_tomados) == 100:
                break
            indice = rn.randint(0,len(ruleta)-1)  
            if indice not in indices_tomados:
                ruleta[indice] = pretendiente
                indices_tomados.append(indice)
                contador+=1
    numrandom = rn.randint(0, len(ruleta)-1)
    masculino = ruleta[numrandom]
    return masculino

def eliminar_masculino(poblacion, masculino):
    for index, ind in enumerate(poblacion):
        if ind.genes == masculino.genes:
            del poblacion[index]
            return poblacion

def puntuar_individuos(poblacion):
    puntuados= []
    for ind in poblacion:
        ind.ajusar_con_bin(MODELO)
        ind.puntuar()
        puntuados.append(ind)
    return puntuados

def seleccionar_padres(poblacion:list):
    poblacion = puntuar_individuos(poblacion)
    # genero numero random
    numrandom = rn.randint(0, len(poblacion)-1)
    # selecciono un femenino
    femenino = poblacion[numrandom]
    # elimino el femenino
    del poblacion[numrandom]
    # calculo la probailidad de los pretendientes
    poblacion = calcular_probabilidad_seleccion(poblacion)
    #selecciono un masculino para la reproduccion
    masculino = seleccionar_masculino(poblacion)
    #elimino el masculino de la poblacion de pretendientes
    poblacion = eliminar_masculino(poblacion, masculino)

    return [femenino, masculino], poblacion

def reproducir(padres:list):
    # defino un punto de corte
    numrandom = rn.randint(1, len(padres[0].binario)-2)
    binario1_p1 = padres[0].binario[:numrandom]
    binario1_p2 = padres[0].binario[numrandom:]

    binario2_p1 = padres[1].binario[:numrandom]
    binario2_p2 = padres[1].binario[numrandom:]

    nuevobin1 = binario1_p1 + binario2_p2
    nuevobin2 = binario1_p2 + binario2_p1

    hijo1 = Individuo(padres[0].genes, nuevobin1)
    hijo2 = Individuo(padres[0].genes, nuevobin2)
    
    return puntuar_individuos([hijo1, hijo2])

def mutar(hijos):
    # selecciono uno de los dos hijos random
    numrandom = rn.randint(0,1)
    hijo = hijos[numrandom]
    del hijos[numrandom]
    numrandom = rn.randint(0,len(hijo.binario)-1)
    hijo.binario[numrandom] = rn.randint(0,1)
    numrandom = rn.randint(0,len(hijo.binario)-1)
    hijo.binario[numrandom] = rn.randint(0,1)
    hijos.append(hijo)
    return hijos


def ver_lista(lista):
    for i in lista:
        i.ver_genes()
