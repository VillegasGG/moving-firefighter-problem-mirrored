import json

# Cargar los datos de los experimentos
with open('resultsChico/experiments_moving_nodes.json', 'r') as f:
    experiments_data = json.load(f)

# Cargar los resultados de los experimentos
with open('resultsChico/results_moving_nodes.json', 'r') as f:
    results_data = json.load(f)

