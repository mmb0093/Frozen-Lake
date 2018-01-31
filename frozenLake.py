import numpy as np
import matplotlib.pyplot as plt
import random
import time
import gym
from gym import wrappers

#Arrancar un episodio
def run_episode(env, jugada, episodios=100):
    puntuacion_total = 0
    obs = env.reset()
    for t in range(episodios):
        accion = jugada[obs]
        obs, puntuacion, done, _ = env.step(accion)
        puntuacion_total += puntuacion
        if done:
            break
    return puntuacion_total
#Generar jugada aleatoria
def generar_jugada_aleatoria():
    return np.random.choice(4, size=((16)))

#Evaluación
def evaluar_jugada(env, jugada, episodios=100):
    puntuacion_total = 0.0
    for _ in range(episodios):
        puntuacion_total += run_episode(env, jugada)
    return puntuacion_total / episodios

#Cruce
def cruce(jugada1, jugada2):
    nueva_jugada = jugada1.copy()
    for i in range(16):
        rand = np.random.uniform()
        if rand > 0.8:
            nueva_jugada[i] = jugada2[i]
    return nueva_jugada

#Mutación
def mutacion(jugada, p=0.1):
    nueva_jugada = jugada.copy()
    for i in range(16):
        rand = np.random.uniform()
        if rand < p:
            nueva_jugada[i] = np.random.choice(4)
    return nueva_jugada

if __name__ == '__main__':
    env = gym.make('FrozenLake-v0')
    env.seed(0)
    numero_jugadas = 100
    generaciones = 20
    puntuacion = []
    #Generamos las jugadas
    generar_jugadas = [generar_jugada_aleatoria() for _ in range(numero_jugadas)]
    for idx in range(generaciones):
        puntuación_jugadas = [evaluar_jugada(env, p) for p in generar_jugadas]
        print('Generación %d : mejor puntuación = %0.2f' % (idx + 1, max(puntuación_jugadas)))
        puntuacion.append(max(puntuación_jugadas))
        #Elitismo



        #Calculamos la probabilidad de cruce
        select_probs = np.array(puntuación_jugadas) / np.sum(puntuación_jugadas)

        #Se genera la descendencia mediante el cruce de 2 individuos.
        child_set = [cruce(
            generar_jugadas[np.random.choice(range(numero_jugadas), p=select_probs)],
            generar_jugadas[np.random.choice(range(numero_jugadas), p=select_probs)])
            for _ in range(numero_jugadas - 20)]
        # Seleccion


        # Se ordenan las jugadas de mejores puntuadas a peores.
        ranking_mejores_jugadas = list(reversed(np.argsort(puntuación_jugadas)))

        # De entre las jugadas de la generación actual escogemos aquellas que son mejores
        elite_set = [generar_jugadas[x] for x in ranking_mejores_jugadas[:10]]

        # Se ordenal las jugadas de peores a mejores y eliminamos los 5 primeros índices
        lista_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        descendientes_sin_peores = np.delete(lista_indices, list(np.argsort(child_set)))


        mutated_list = [mutacion(p) for p in descendientes_sin_peores]
        generar_jugadas = elite_set
        generar_jugadas += mutated_list

    puntuación_jugada = [evaluar_jugada(env, p) for p in generar_jugadas]

    #Representación
    plt.plot(puntuacion)
    plt.show()


    env.close()
