 
![n](https://github.com/mmb0093/Frozen-Lake/blob/master/img/logo_burgos.png)

*Práctica perteneciente a la asignatura de Computación neuronal y Evolutiva, Grado en Informática, Universidad de Burgos*.

***Alumnos:** Marta Monje Blanco e Iván Iglesias Cuesta.*

# Algoritmo genético para resolver Frozen Lake

![N](https://github.com/mmb0093/Frozen-Lake/blob/master/img/openai.png)

Este código implementa un **algoritmo genético** que soluciona el **juego Frozen Lake**.

## Prerrequisitos
Antes de clonar el repositorio tenemos que instalar [gym](https://github.com/openai/gym), una librería perteneciente al conjunto de herramientas [OpenAI](https://github.com/openai).

Dado que *Frozen lake* no tiene dependencias, se puede realizar (y se recomienda) hacer la instalación mínima.

Se necesita tener una versión de Python 3.5 o superior. Yo he usado Python 3.6.3.

## Clona el repositorio

Puedes directamente clonarlo desde el propio repositorio o desde consola:

	  git clone https://github.com/mmb0093/Frozen-Lake.git
	
## Descripción del juego

Es un juego para un solo jugador en el que hay que llegar desde la casilla de salida a la casilla objetivo, procurando no caer en ningún agujero. El resto de casillas son hielo.

![img](https://github.com/mmb0093/Frozen-Lake/blob/master/img/tablero.png)

El tamaño del tablero va a ser de 4x4, es decir, tiene 16 casillas.

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

Esta función la vamos a emplear para evaluar las jugadas que se van a ir realizando:

	    def evaluar_jugada(env, jugada, episodios=eps):
		puntuacion_total = 0.0
		for _ in range(episodios):
		   puntuacion_total += run_episode(env, jugada)
	    return puntuacion_total / episodios
Devuelve la puntuación media de los episodios.

### Cruce
En la función de cruce recibimos dos jugadas y las cruzamos en función de porcentaje que hayamos establecido en los parámetros:

		def cruce(jugada1, jugada2):
		    nueva_jugada = jugada1.copy()
		    for i in range(tam):
			rand = np.random.uniform()
			if rand > crx:
			    nueva_jugada[i] = jugada2[i]
		    return nueva_jugada
		    
Devuelve la jugada producto del cruce.

### Mutación
Le pasamos la jugada que queremos mutar y la probabilidad de mutación y en función de esta probabilidad se mutará la jugada o no.

		def mutacion(jugada, p=mut):
		    nueva_jugada = jugada.copy()
		    for i in range(tam):
			rand = np.random.uniform()
			if rand < p:
			    nueva_jugada[i] = np.random.choice(act)
		    return nueva_jugada
		    
Devuelve la nueva jugada con la mutación.

A la hora de escoger la probabilidad de mutación hemos de tener en cuenta que ponerlo muy alto puede ser perjudicial. En el caso de este algoritmo no lo subiría de 0.05 en la práctica.


## Experimentación
### Configuración 1
La primera configuración que vamos a explorar es la que hemos dado en el ejemplo de arriba:
		
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
	
	#Elitismo. 
	elit = 50
La gráfica obtenida es la siguiente:

![Gráfica primer experimento](https://github.com/mmb0093/Frozen-Lake/blob/master/img/primeraprueba.png)

Vemos que aprende ya que la gráfica es creciente pero no parece suficiente, es muy irregular.

Repasemos los parámetros de uno en uno:

Si subimos el número de episodios por generación, tendremos más probabilidad de encontrarnos con mejores soluciones, podemos subirlo a 150.

El tamaño del tablero no nos compete por ahora, ni tampoco el número de acciones.

La mutabilidad es muy baja y de momento interesa tenerla así, así que no la voy a modificar, lo mismo para el cruce.

El número de generaciones sí que interesa elevarlo, creo que estaría mejor si lo doblo a 100.

También voy a subir el número de jugadas por generación a 150.

El elitismo es muy alto, lo voy a bajar a 10, porque nos vamos a quedar con las 50 mejores soluciones de 150 y me parece excesivo.

### Configuración 2

Dadas las anteriores conclusiones, la configuración se va a ver así:
		
		#número de episodios
		eps = 150

		#Tamaño del tablero del juego
		tam = 16

		#Mutabilidad
		mut = 0.025

		#Número de acciones (u,d,l,r)
		act = 4

		#Cruce
		crx = 0.6

		#Número de generaciones
		ngen = 100

		#Número de jugadas
		njds = 150

		#Elitismo. 
		elit = 10
Según lo estoy ejecutando, puedo ya darme cuenta de que el tiempo de procesamiento se va de las manos. Es probable que lo haya sobrecargado al aumentar los episodios por jugada, las jugadas por generación y evidentemente, haber metido tantas generaciones.

![Segundo experimento](https://github.com/mmb0093/Frozen-Lake/blob/master/img/segundaprueba.png)

Aprende demasiado rápido y hago inciso en la palabra *demasiado*. Esto implica que lo estamos forzando mucho. Está claro que aunque aprenda muy rápido, los 15 minutos que ha tardado en ejecutarse son intolerables (en comparación con otras pruebas hechas sobre el mismo algoritmo, el cual en menos de un minuto lo suele tener).

Para evitar esta situación de nuevo voy a dejar el número de jugadas y el de episodios como al principio y voy a bajar el número de generaciones a 40.

Voy a dejar la mutación como está, pero el cruce lo voy a subir a 0.75, creo que 0.6 puede ser un poco bajo.

En cuanto al elitismo creo que ya que he bajado el número de jugadas, lo voy a dejar en 10.

### Configuración 3
Configuramos de nuevo:

		#número de episodios
		eps = 100

		#Tamaño del tablero del juego
		tam = 16

		#Mutabilidad
		mut = 0.025

		#Número de acciones (u,d,l,r)
		act = 4

		#Cruce
		crx = 0.75

		#Número de generaciones
		ngen = 44

		#Número de jugadas
		njds = 100

		#Elitismo. 
		elit = 10
		
Nuevamente, mientras estoy ejecutando veo que vuelve la fluided, entonces podemos concluir que el problema del tiempo y la sobrecarga estaba donde se pensaba.

![Tercera prueba](https://github.com/mmb0093/Frozen-Lake/blob/master/img/terceraprueba.png)

Ya vemos que llega a soluciones igual de buenas y hemos reducido tiempos sin que la calidad de las respuestas se hayan visto afectadas.

Esta solución me parece perfectamente factible, pero para que no se quede ningún parámetro por tocar y para dar algún matiz vamos a modificar lo siguiente:

Voy a subir la mutabilidad, no mucho, pero la vamos a dejar en 0.06.

Lo otro con lo que quiero jugar es con el elitismo, lo voy a dejar a 0.


### Configuración 4

La cuarta configuración se va a ver así:

		#número de episodios
		eps = 100

		#Tamaño del tablero del juego
		tam = 16

		#Mutabilidad
		mut = 0.06

		#Número de acciones (u,d,l,r)
		act = 4

		#Cruce
		crx = 0.75

		#Número de generaciones
		ngen = 44

		#Número de jugadas
		njds = 100

		#Elitismo.
		elit = 0
		
Mientras va ejecutando puedo afirmar que la velocidad es la misma que la anterior, de hecho, quizá un poco más rápida debido a que está sin elitismo.

![Cuarta prueba](https://github.com/mmb0093/Frozen-Lake/blob/master/img/pruebacuarta.png)

Podemos observar que ha perdido homogeneidad, sobre todo al principio de la curva de aprendizaje y es bastante evidente porque el elitismo (en bajas dósis) beneficia al aprendizaje ya que guarda buenas soluciones sin impedir que se generen nuevas.
Aun así el resultado final de aprendizaje es muy similar.

Voy a repetir el mismo experimento con la misma configuración, pero esta vez, voy a subir el eliismo a 15, a ver que pasa


## Configuración final
La configuración que va a quedar es esta:

			#número de episodios
			eps = 100

			#Tamaño del tablero del juego
			tam = 16

			#Mutabilidad
			mut = 0.06

			#Número de acciones (u,d,l,r)
			act = 4

			#Cruce
			crx = 0.75

			#Número de generaciones
			ngen = 40

			#Número de jugadas
			njds = 100

			#Elitismo. de todas las jugadas, nos quedamos con algunas de las mejores
			#Hay que tener especial cuidado en que este número no supere el número de jugadas
			elit = 15

El resultado gráfico es este:

![Configuración final](https://github.com/mmb0093/Frozen-Lake/blob/master/img/final.png)

Vemos que el aprendizaje se suaviza al principio (debido al elitismo) y que aprende igual de bien que las anteriores pruebas en menos tiempo de ejecución.

Aun con todo esto yo bajaría el número de generaciones, no creo que hagan falta tantas (quizá 30 sean suficientes).


## Librerías complementarias

Lo bueno de la librería Gym de OpenAI es que hay muchas librerías preparadas para cubrir sus funcionalidades.

Investigando un poco se puede ver que hay muchas favoritas como [Tensorflow](https://github.com/tensorflow/tensorflow) o [Theano](https://github.com/Theano).

Yo me he topado con [Simple DQN](https://github.com/tambetm/simple_dqn). No es de las más fáciles que he visto pero se usa bastante.
Obviamente hay muchas más, aun que no es estrítamente necesario, recomiento usar alguna, más que nada porque aunque tengas que gastar tiempo en aprender a usarlas, te va ha ahorrar algún que otro dolor de cabeza (o no).

## Conclusiones

Hemos visto el potencial de lo que Gym nos puede ofrecer, hay librerías que implementan más juegos y más modelos (aunque dan bastantes problemas dependiendo del OS que estés usando), pero en concreto este juego y el Cart Pole, son los mejores para hacer ejemplos porque no tienen dependencia externas.

A la hora de ajustar un algoritmo para una solución en concreto hemos de ser conscientes de que las soluciones no van a ser genéricas, dependen de lo que se esté intentando resolver y los parámetros usados son totalmente experimentales, no hay "normas" para escoger de manera crítica más allá de la observación y el sentido común.

Otro factor a tener en cuenta es cómo vamos a premiar o castigar una solución en función de su adaptación. Saber encontrar el equilibrio entre "zanahorias" y "latigazos" es importante. En ente caso, el algoritmo presentado "premia" en función de la adaptación de cada individuo.

El elitismo es otro punto crítico. En el algoritmo que usamos, el elitismo se queda con las mejores soluciones pero hay más formas, de hecho, una buena propuesta sería quedarse con los mejores de la solución antigua y sustituir los que tengan peor adaptación en la descendencia (quizá sea muy elitista, pero se puede hacer).

