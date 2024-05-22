class SimulationRepository:
    def __init__(self):
        self.simulations = []

    def save_simulation(self, simulation):
        self.simulations.append(simulation)

    def get_simulations(self):
        return self.simulations
