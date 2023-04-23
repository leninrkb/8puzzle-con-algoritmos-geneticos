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
poblacion = al.generar_poblacion(semilla=Individuo(gen_semilla, binario), densidad=200)
poblacion = al.seleccionar_poblacion_inicial(poblacion, (20,50))

contador = 0
seguir = True
while seguir:
    padres, poblacion = al.seleccionar_padres(poblacion)
    hijos = al.reproducir(padres)
    hijos = al.mutar(hijos)
    contador+=1
    poblacion = poblacion + hijos
    print(contador)
    print(f'** bin\n{hijos[0].binario}\n{hijos[1].binario}\n')
    seguir = al.revisar_mejores_genes(poblacion)
    