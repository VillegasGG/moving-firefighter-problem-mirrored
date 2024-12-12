import json
import plotly.graph_objects as go

# Cargar los datos de los experimentos
with open('resultsChico/experiments_moving_nodes.json', 'r') as f:
    experiments_data = json.load(f)

# Cargar los resultados de los experimentos
with open('resultsChico/results_moving_nodes.json', 'r') as f:
    results_data = json.load(f)

def get_experiment_by_id(experiment_id, experiments_data):
    for experiment in experiments_data:
        if experiment['id'] == experiment_id:
            return experiment
    return None

def get_result_by_experiment_id(experiment_id, method_results):
    for result in method_results:
        if result['experiment'] == experiment_id:
            return result
    return None

def plot_experiment(experiment_id, method, experiments_data, results_data, save_path_prefix=None):
    experiment = get_experiment_by_id(experiment_id, experiments_data)
    if(experiment == None):
        print(f"No results found for experiment {experiment_id}")
        return
    
    method_results = results_data[method] 
    if method_results == None:
        print(f"No results found for method {method}")
        return

    # Encontrar el resultado correspondiente al experimento
    result = get_result_by_experiment_id(experiment_id, method_results)
    
    if result is None:
        print(f"No results found for experiment {experiment_id}")
        return

    # Extraer las posiciones de los nodos y lista de posiciones del bombero
    nodes_positions = experiment['nodes_positions']
    firefighter_positions = result['solution']


# Graficar y guardar cada paso de un experimento específico
plot_experiment(1, 'dynamic_programming', experiments_data, results_data, save_path_prefix='experiment_1')