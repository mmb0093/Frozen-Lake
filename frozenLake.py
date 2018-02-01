import numpy as np
import matplotlib.pyplot as plt
import random
import time
import gym
from gym import wrappers

#número de episodios
eps = 100

#Tamaño del tablero del juego
tam = 16

#Mutabilidad
mut = 0.025

#Número de acciones (u,d,l,r)
act = 4

#Cruce
crx = 0.6

#Número de generaciones
ngen = 50

#Número de jugadas
njds = 100

#Elitismo. de todas las jugadas, nos quedamos con algunas de las mejores
#Hay que tener especial cuidado en que este número no supere el número de jugadas
elit = 50

#Arrancar un episodio
def run_episode(env, jugada, episodios=eps):
    puntuacion_total = 0
    obs = env.reset()
    for t in range(episodios):
        # La siguiente línea de código permite que en la ejecución se vean las jugadas con tablero
        #Hay que tener cuidado porque si se sobrecarga el algoritmo se verá afectado el tiempo de ejecución
        #env.render()
        accion = jugada[obs]
        obs, puntuacion, done, _ = env.step(accion)
        puntuacion_total += puntuacion
        if done:
            break
    return puntuacion_total
#Generar jugada aleatoria
def generar_jugada_aleatoria():
    return np.random.choice(act, size=((tam)))

#Evaluación
def evaluar_jugada(env, jugada, episodios=eps):
    puntuacion_total = 0.0
    for _ in range(episodios):
        puntuacion_total += run_episode(env, jugada)
    return puntuacion_total / episodios

#Cruce
def cruce(jugada1, jugada2):
    nueva_jugada = jugada1.copy()
    for i in range(tam):
        rand = np.random.uniform()
        if rand > crx:
            nueva_jugada[i] = jugada2[i]
    return nueva_jugada

#Mutación
def mutacion(jugada, p=mut):
    nueva_jugada = jugada.copy()
    for i in range(tam):
        rand = np.random.uniform()
        if rand < p:
            nueva_jugada[i] = np.random.choice(act)
    return nueva_jugada

if __name__ == '__main__':
    env = gym.make('FrozenLake-v0')
    env.seed(0)
    numero_jugadas = njds
    generaciones = ngen
    puntuacion = []
    #Generamos las jugadas
    generar_jugadas = [generar_jugada_aleatoria() for _ in range(numero_jugadas)]
    for idx in range(generaciones):
        puntuación_jugadas = [evaluar_jugada(env, p) for p in generar_jugadas]
        print('Generación %d : mejor puntuación = %0.2f' % (idx + 1, max(puntuación_jugadas)))
        puntuacion.append(max(puntuación_jugadas))
        #Elitismo


        probabilidad_seleccion = np.array(puntuación_jugadas) / np.sum(puntuación_jugadas)


        #Se genera la descendencia mediante el cruce de 2 individuos.
        child_set = [cruce(
            generar_jugadas[np.random.choice(range(numero_jugadas), p=probabilidad_seleccion)],
            generar_jugadas[np.random.choice(range(numero_jugadas), p=probabilidad_seleccion)])
            for _ in range(numero_jugadas -elit )]

        # Seleccion

        # Se ordenan las jugadas de mejores puntuadas a peores.
        ranking_mejores_jugadas = list(reversed(np.argsort(puntuación_jugadas)))

        # De entre las jugadas de la generación actual escogemos aquellas que son mejores
        elite_set = [generar_jugadas[x] for x in ranking_mejores_jugadas[:elit]]

        #Mutamos
        mutated_list = [mutacion(p) for p in child_set]



        #Sumamos la lista de mutaciones a los mejores individuaos de la generación anterior
        generar_jugadas = elite_set
        generar_jugadas += mutated_list



    puntuación_jugada = [evaluar_jugada(env, p) for p in generar_jugadas]

    #Representación
    plt.plot(puntuacion)
    plt.ylabel("Fitness")  # Inserta el título del eje X
    plt.xlabel("Generación")  # Inserta el título del eje Y
    plt.title("Aprendizaje")
    plt.show()


    env.close()
