from individuo import Individuo
import numpy as np
import algoritmo as al

gen_semilla = [
    [2,3,4],
    [0,1,7],
    [8,6,5],
]
gen_semilla = np.array(gen_semilla).flatten().tolist()
binario = al.calcular_binario(gen_semilla)
poblacion = al.generar_poblacion(semilla=Individuo(gen_semilla, binario), densidad=20)
poblacion = al.seleccionar_poblacion_inicial(poblacion, (4,6))

contador = 0
seguir = True
while seguir:
    padres, poblacion = al.seleccionar_padres(poblacion)
    hijos = al.reproducir(padres)
    hijos = al.mutar(hijos)
    contador+=1
    poblacion = poblacion + hijos
    print(contador)
    print(f'** bin: {hijos[0].binario}')
    for h in hijos:
        h.puntuar()
        if h.puntuacion >= 8:
            print(f'solucion encontrada:\n {h.ver_genes()}')
            seguir = False
            break