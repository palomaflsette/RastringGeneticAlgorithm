import numpy as np
from geneticalgorithm2 import geneticalgorithm2 as ga
from geneticalgorithm2 import Callbacks
from geneticalgorithm2 import Population_initializer


class GeneticAlgorithmService:
    def __init__(self, function, dimensions, varbound, algorithm_params):
        self.function = function
        self.dimensions = dimensions
        self.varbound = varbound
        self.algorithm_params = algorithm_params
        self.model = None

    def initialize_model(self):
        self.model = ga(
            function=self.function.evaluate,
            dimension=self.dimensions,
            variable_type='real',
            variable_boundaries=self.varbound,
            algorithm_parameters=self.algorithm_params
        )

    def run(self, num_experimentos):
        simulacoes = []
        for simu in range(num_experimentos):
            print()
            print('-------------------------------------------------------------------')
            print('Experimento número = ', simu)
            self.model.run(
                no_plot=False,
                disable_progress_bar=False,
                set_function=None,
                apply_function_to_parents=False,
                start_generation={'variables': None, 'scores': None},
                studEA=True,
                mutation_indexes=None,
                init_creator=None,
                init_oppositors=None,
                duplicates_oppositor=None,
                remove_duplicates_generation_step=2,
                revolution_oppositor=None,
                revolution_after_stagnation_step=None,
                revolution_part=0,
                population_initializer=Population_initializer(
                    select_best_of=1,
                    local_optimization_step='never',
                    local_optimizer=None
                ),
                stop_when_reached=None,
                callbacks=[
                    Callbacks.SavePopulation(
                        'infraestructure/files/callback_pop_example', save_gen_step=1, file_prefix='constraints'),
                    Callbacks.PlotOptimizationProcess(
                        'infraestructure/files/callback_plot_example', save_gen_step=300, show=False, main_color='red', file_prefix='plot')
                ],
                middle_callbacks=[],
                time_limit_secs=None,
                save_last_generation_as=None,
                seed=None
            )

            if hasattr(self.model, 'result'):
                self.model.plot_generation_scores()
            else:
                print("No result available for plotting.")

            convergence = self.model.report
            print("melhores indivíduos por geração", convergence)
            simulacoes.append(convergence)
        return simulacoes
