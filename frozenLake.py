import numpy as np
import random
import time
import gym
from gym import wrappers

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
        if rand > 0.5:
            nueva_jugada[i] = jugada2[i]
    return nueva_jugada

#Mutación
def mutacion(jugada, p=0.05):
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
    numero_pasos = 20
    policy_pop = [generar_jugada_aleatoria() for _ in range(numero_jugadas)]
    for idx in range(numero_pasos):
        puntuación_jugadas = [evaluar_jugada(env, p) for p in policy_pop]
        print('Generación %d : mejor puntuación = %0.2f' % (idx + 1, max(puntuación_jugadas)))
        # Se ordenal las jugadas de peores a mejores
        ranking_peores_jugadas = list(np.argsort(puntuación_jugadas))
        # elitismo
        # Se ordenan las jugas de mejores puntuadas a peores.
        ranking_mejores_jugadas = list(reversed(np.argsort(puntuación_jugadas)))
        # De entre las jugadas aleatorias de un episodio escogemos aquellas que son mejores
        elite_set = [policy_pop[x] for x in ranking_mejores_jugadas[:20]]
        select_probs = np.array(puntuación_jugadas) / np.sum(puntuación_jugadas)
        child_set = [cruce(
            policy_pop[np.random.choice(range(numero_jugadas), p=select_probs)],
            policy_pop[np.random.choice(range(numero_jugadas), p=select_probs)])
            for _ in range(numero_jugadas - 20)]
        mutated_list = [mutacion(p) for p in child_set]
        policy_pop = elite_set
        policy_pop += mutated_list
    policy_score = [evaluar_jugada(env, p) for p in policy_pop]

    env.close()
