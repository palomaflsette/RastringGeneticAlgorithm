import matplotlib.pyplot as plt
from domain.entities.function import RastriginFunction
from domain.services.genetic_algorithm_service import GeneticAlgorithmService
from infraestructure.common.file_simulation_repository import FileSimulationRepository
from application.use_cases.run_simulation_use_case import RunSimulationUseCase
import numpy as np
import pandas as pd


def main():
    dimensions = 2

    file_path = 'simulations.json'

    num_experimentos = 5

    rastrigin_function = RastriginFunction(dimensions)
    simulation_repository = FileSimulationRepository(file_path)

    algorithm_params = {
        'max_num_iteration': 1,
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

    iteration_numbers = [10, 20, 50]
    GeneticAlgorithm('max_num_iteration',
                    iteration_numbers,
                    dimensions,
                    num_experimentos,
                    algorithm_params,
                    rastrigin_function,
                    simulation_repository)


def GeneticAlgorithm(param_name: str, list_of_params: list,
                    dimensions: int,
                    num_of_experiments: int,
                    base_algorithm_params: dict, function,
                    simulation_repo):
    results = {}
    varbound = np.array([[-5.12, 5.12]] * dimensions)

    for param in list_of_params:
        algorithm_params = base_algorithm_params.copy()
        algorithm_params[param_name] = param

        genetic_algorithm_service = GeneticAlgorithmService(
            function,
            dimensions, varbound,
            algorithm_params)

        run_simulation_use_case = RunSimulationUseCase(
            genetic_algorithm_service, simulation_repo)

        simulacoes = run_simulation_use_case.execute(num_of_experiments)

        # Análise dos resultados
        max_iterations = algorithm_params['max_num_iteration']
        mean_simulation = [0] * max_iterations

        for i in range(max_iterations):
            soma_sim_geracao = 0
            for j in range(num_of_experiments):
                if i < len(simulacoes[j]):
                    soma_sim_geracao += simulacoes[j][i]
            mean_simulation[i] = soma_sim_geracao / num_of_experiments

        results[param] = mean_simulation
        print(
            f'{param_name}: {param}, Média dos Melhores por Geração: {mean_simulation}')

    # Criação da Tabela de Resultados
    max_iterations = max(
        [base_algorithm_params['max_num_iteration']] + [len(r) for r in results.values()])
    data = {
        'Geração': list(range(1, max_iterations + 1))
    }
    for param in list_of_params:
        mean_simulation = results[param]
        if len(mean_simulation) < max_iterations:
            mean_simulation += [None] * (max_iterations - len(mean_simulation))
        data[f'{param_name} {param}'] = mean_simulation

    df = pd.DataFrame(data)
    print(df)

    # Plotando os resultados
    fig1, ax1 = plt.subplots()
    for param, mean_simulation in results.items():
        ax1.plot(mean_simulation, label=f'{param_name} {param}')
    ax1.set_title('Média dos Melhores por Geração')
    ax1.set_xlabel('Geração')
    ax1.set_ylabel('Valor da Função')
    ax1.legend()
    plt.show()

    #return df


if __name__ == '__main__':
    main()
