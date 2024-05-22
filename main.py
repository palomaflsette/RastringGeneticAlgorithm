# main.py
import matplotlib.pyplot as plt
from domain.entities.function import RastriginFunction
from domain.services.genetic_algorithm_service import GeneticAlgorithmService
from infraestructure.common.file_simulation_repository import FileSimulationRepository
from application.use_cases.run_simulation_use_case import RunSimulationUseCase
import numpy as np

# Configuração dos parâmetros
dimensions = 2
varbound = np.array([[-5.12, 5.12]] * dimensions)

algorithm_params = {
    'max_num_iteration': 10,
    'population_size': 10,
    'mutation_probability': 0.001,
    'elit_ratio': 0.2,
    'crossover_probability': 0.6,
    'parents_portion': 0.8,
    'crossover_type': 'one_point',
    'max_iteration_without_improv': None,
    'mutation_type': 'uniform_by_center',
    'selection_type': 'roulette'
}

num_experimentos = 5
file_path = 'simulations.json'

# Instanciação das entidades, serviços e repositórios
rastrigin_function = RastriginFunction(dimensions)
genetic_algorithm_service = GeneticAlgorithmService(
    rastrigin_function, dimensions, varbound, algorithm_params)
simulation_repository = FileSimulationRepository(file_path)

# Caso de uso para executar a simulação
run_simulation_use_case = RunSimulationUseCase(
    genetic_algorithm_service, simulation_repository)

# Executar a simulação e salvar os resultados
simulacoes = run_simulation_use_case.execute(num_experimentos)

# Análise dos resultados
mean_simulation = []
for i in range(algorithm_params['max_num_iteration']):
    soma_sim_geracao = 0
    for j in range(num_experimentos):
        soma_sim_geracao += simulacoes[j][i]
    mean_simulation.append(soma_sim_geracao / num_experimentos)

print('------------------------------------------------------------------------')
print('Valores médios dos melhores por Geração')
print(mean_simulation)

fig1, ax1 = plt.subplots()
ax1.set_title('Media dos Melhores por Geração')
ax1.boxplot(mean_simulation)
plt.show()

plt.plot(mean_simulation, label='Média dos Melhores por Geração')
plt.legend(loc='upper right')
plt.show()
