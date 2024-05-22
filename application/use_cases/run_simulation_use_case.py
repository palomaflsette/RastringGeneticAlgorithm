class RunSimulationUseCase:
    def __init__(self, genetic_algorithm_service, simulation_repository):
        self.genetic_algorithm_service = genetic_algorithm_service
        self.simulation_repository = simulation_repository

    def execute(self, num_experimentos):
        self.genetic_algorithm_service.initialize_model()
        simulacoes = self.genetic_algorithm_service.run(num_experimentos)
        for simulacao in simulacoes:
            self.simulation_repository.save_simulations(simulacao)
        return simulacoes