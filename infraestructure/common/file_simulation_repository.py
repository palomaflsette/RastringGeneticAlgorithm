import os
import json

class FileSimulationRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_simulations(self, simulations):
        with open(self.file_path, 'w') as f:
            json.dump(simulations, f)

    def load_simulations(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return []
