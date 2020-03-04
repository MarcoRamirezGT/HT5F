#Eduardo Ramírez Herrera 19946
#Simulacion de la ejecucion de procesos en una computadora con RAM y CPU. 

import simpy
import random

#Funcion para la ejecucion de procesos
def processes(name, env,arrivalT, cpu, ram, waiting):
    
    global totalT #Variable global para el tiempo que le toma ejecutar todos los procesos
    global processT #Lista para almacenar cuanto le tomo a cada proceso y poder calcular la desviacion estandar
    
    yield env.timeout(arrivalT) #Tiempo de llegada, determinado por la distribucion aleatoria
    startT = env.now #Momento en el que inicia el procesamiento del proceso
    departureT = 0
    print (' Proceso %d en el tiempo %s ' % (name, startT))
    
    procesdeata = random.randint(1,200) #Asignacion de la cantidad de instrucciones del proceso
    ram_needed = random.randint(1,10) #Asignacion de la cantidad de memoria que necesita el proceso
    
    with ram.get(ram_needed) as queue1:
        
        print ('Proceso %d entra a la RAM en %s' % (name, env.now))
        print ('Ocupa %d en la RAM: %s' % (name, ram_needed))
        
        while procesdeata>0:
            
            with cpu.request() as queue2: #Uso del CPU como recurso con colas
                
                yield queue2
                print ('Proceso %d entra al CPU en %s' % (name, env.now))
                
                yield env.timeout(1)
                procesdeata = procesdeata -3 #Ejecucion del CPU de 3 instrucciones del proceso
                
                if procesdeata<=0: #Saca el proceso de la computadora, ya que esta terminado
                    
                    procesdeata = 0
                    departureT = env.now 
                    print ('Proceso %d sale del CPU en el momento %s' %(name,departureT))
                    
                else: #Determina si el proceso entra directamente al CPU nuevamente si todavia tiene instrucciones o si debe hacer cola
                    
                    alternData = random.randint(1,2)
                    
                    if alternData == 1:
                        
                        with waiting.request() as queue3:
                            
                            yield queue3
                            yield env.timeout(1)
                            
    timeTotalData = departureT - startT #Tiempo que le tomo ejecutar el proceso
    processT.append(timeTotalData) #Se agrega el tiempo a la lista de tiempos
    totalT = departureT #Se actualiza el tiempo total

#Funcion para calcular la desviacion estandar                            
def desviacionEstandar (data, average):
    
    totaldE = 0
    for i in range(len(data)):
        
        totaldE = (data[i]-average)**2
        
    de = (totaldE/(len(data)-1.0))**(0.5)
    
    return de


#Creacion de las variables necesarias para la simulacion

env = simpy.Environment()
ram = simpy.Container(env, capacity=100)
cpu = simpy.Resource(env, capacity=1)
waiting = simpy.Resource(env, capacity = 1)
random.seed(12345)
interval = 10.0
totalT = 0
processT = []
totalDataProcess=25

#Implementacion de la funcion de processing
for i in range (totalDataProcess):
    
    env.process(processes(i,env,random.expovariate(1.0/interval),cpu,ram,waiting))

#Ejecucion de la simulacion
env.run()
Average = float(totalT)/float(totalDataProcess)
desviacionEstandar = desviacionEstandar(processT,Average)

#Mostrar datos obtenidos
print ('Tiempo total: %d \nPromedio de tiempo por instruccion: %s \nDesviacion Estandar: %f' % (totalT, Average, desviacionEstandar))
