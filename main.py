#Hoja de Trabajo 5
#Jorge Luis Lopez 221038
'objetivos: '
#Simulación DES (Discrete Event Simulation) usando el módulo SimPy.
# Utilización de colas con la clase Resources y Container de SimPy.

import simpy
import random
import statistics
import math

process_times = [4, 8, 12, 16 ]
RANDOM_SEED=20
Procesos=25
Memoria=100

def function(env, Tproceso, codigo, RAM, memUtilizar, Instrucciones, InsPorMin):
    
    #Tiempo de llegada
    yield env.timeout(Tproceso)
    print('Tiempo: %f - %s se solicita %d de RAM' % (env.now, codigo, memUtilizar))
    #tiempos.append(math.floor(Tproceso)) #Agregar tiempos a la lista

    
    #Empezar tiempo
    Tllegada = env.now

    #Solicitud de espacio a la RAM
    yield RAM.get(memUtilizar) #Solicitar memoria a la RAM
    print('Tiempo: %f - %s (Solicitud de RAM) %d de RAM,aceptada' % (env.now, codigo, memUtilizar))


    #Instrucciones que se completaron
    CompletedIns=0
    
    #Inicializar el CPU
    with CPU.request() as req:
        yield req
        #Obtener instrucciones totales a realizar
        if(Instrucciones>=InsPorMin):
            #Instrucciones a realizar
            InsRealizar = InsPorMin
        else:
            #Si las instrucciones son menores a 3
            InsRealizar = Instrucciones-CompletedIns
            
        #Tomamos el tiempo para realizar la Instruccion
        yield  env.timeout(InsRealizar/InsPorMin)
        
        #Se actualiza las Instrucciones completadas
        CompletedIns += InsRealizar
        
        #Se genera un random para ver si repite el proceso o sale
        cont = random.randint(1,2)
        if cont == 1 and InsRealizar<InsPorMin:
            with Espera.request() as reqE:
                yield reqE
                
            yield env.timeout(1)
            #Se devuelve la memoria utilizada a la RAM
            yield RAM.put(memUtilizar)
            print("Se finalizo el proceso %f - %s, se utilizo solo %d de Memoria RAM" % (env.now, codigo, memUtilizar))
            
           
random.seed(RANDOM_SEED)
env = simpy.Environment()
RAM = simpy.Container(env, init = Memoria, capacity= 100)
CPU = simpy.Resource(env, capacity = 1)
Espera = simpy.Resource(env, capacity = 1)
InsPorMin = 3.0
constante = 1

def stats():
    print()
    print('---Stadisticas:---')
    print()
    print(f'✓ Average execution time: {statistics.mean(process_times)}')
    print(f'✓ Standard Deviation: {statistics.pstdev(process_times)}')

#Se crea un nuevo proceso
for i in range(Procesos):
    Tproceso = random.expovariate(1.0/constante)
    memUtilizar= random.randint(1, 10)  #Memoria a solicitar
    Instrucciones= random.randint(1, 10) #Intrucciones que necesitaran 
    env.process(function(env, Tproceso,"Proceso %d" % i,RAM, memUtilizar,Instrucciones,InsPorMin))
   
#Comienza el proceso de ejecucion
env.run()
#Corre las estadisticas
stats()