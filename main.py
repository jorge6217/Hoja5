#Hoja de Trabajo 5
#Jorge Luis Lopez 221038
'objetivos: '
#Simulación DES (Discrete Event Simulation) usando el módulo SimPy.
# Utilización de colas con la clase Resources y Container de SimPy.

import simpy
import random

RANDOM_SEED = 123

INTERVAL_CREATION = 10
NUM_CORES = 1
INSTRUCTIONS_PER_CYCLE = 3
RAM_SIZE = 100
PROCESS_COUNT = 25

class Process:
    def __init__(self, env, ram, cpu, process_id, instructions_per_cycle):
        self.env = env
        self.ram = ram
        self.cpu = cpu
        self.process_id = process_id
        self.instructions_per_cycle = instructions_per_cycle

    def run(self):
        process_time = 0
        while self.ram.level >= self.instructions_per_cycle:
            with self.cpu.request() as request:
                yield request
                self.ram.get(self.instructions_per_cycle)
                process_time += 1
                yield self.env.timeout(1)
                self.ram.put(self.instructions_per_cycle)
        return process_time

def simulation(env, ram, cpu, interval_creation, num_cores, instructions_per_cycle, ram_size, process_count):
    print()
    print('---SIMULATION STARTED---')
    print()
    process_times = []
    for process_id in range(1, process_count+1):
        next_process_time = random.expovariate(1.0 / interval_creation)
        yield env.timeout(next_process_time)
        process = Process(env, ram, cpu, process_id, instructions_per_cycle)
        env.process(process.run())
        process_time = yield process.run()
        process_times.append(process_time)
    return process_times

random.seed(RANDOM_SEED)
env = simpy.Environment()
ram = simpy.Container(env, capacity=RAM_SIZE, init=RAM_SIZE)
cpu = simpy.Resource(env, capacity=NUM_CORES)

process_times = env.run(until=simulation(env, ram, cpu, INTERVAL_CREATION, NUM_CORES, INSTRUCTIONS_PER_CYCLE, RAM_SIZE, PROCESS_COUNT))

from stats import showData
showData(process_times)
