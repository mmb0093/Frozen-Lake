# Algoritmo genético para resolver Frozen Lake

![N](https://github.com/mmb0093/Frozen-Lake/blob/master/img/openai.png)

Este código implementa un **algoritmo genético** que soluciona el **juego Frozen Lake**.

## Prerrequisitos
Antes de clonar el repositorio tenemos que instalar [gym](https://github.com/openai/gym), una librería perteneciente al conjunto de herramientas [OpenAI](https://github.com/openai).
Dado que *Frozen lake* no tiene dependencias, se puede realizar (y se recomienda) hacer la instalación mínima.

Se necesita tener una versión de Python 3.5 o superior. Yo he usado Python 3.6.3.
## Conceptos y teoría
## Clona el repositorio
Puedes directamente clonarlo desde el propio repositorio o desde consola:

	  git clone https://github.com/mmb0093/Frozen-Lake.git
	
## Descripción del juego
Es un juego para un solo jugador en el que hat que llegar desde la casilla de salida a la casilla objetivo, procurando no caer en ningún agujero. El resto de casillas son hielo.
![img](https://github.com/mmb0093/Frozen-Lake/blob/master/img/tablero.png)

El tamaño del tablero va ha ser de 4x4, es decir, tiene 16 casillas.
Los posibles movimientos son 4:
  - Arriba (u)
  - Abajo (d)
  - Derecha (r)
  - Izquierda (l)
## Estructura del código
### Parámetros

Los parámetros que vamos a emplear para ajustar el algoritmo:

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

### Evaluación

Esta función la vamos a emplear para evaluar las jugadas que se van a ir reslizando.
    def evaluar_jugada(env, jugada, episodios=eps):
        puntuacion_total = 0.0
        for _ in range(episodios):
           puntuacion_total += run_episode(env, jugada)
    return puntuacion_total / episodios

### Cruce

### Mutación
## Experimentación
### Configuración 1
### Configuración 2
### Configuración 3
### Configuración 4
## Librerías complementarias
## Conclusiones
