import algoritmo as al

poblacion = al.generar_poblacion(10)
poblacion_inical = al.seleccionar_poblacion_inicial(poblacion,(4,10))

al.seleccionar_padres(poblacion_inical)