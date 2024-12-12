import json
import plotly.graph_objects as go
from fire_simulation import FirePropagation
from utils import Tree
from tree_visualizer import TreeVisualizer

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
    
    # Cargar datos del árbol
    with open('trees/tree_' + str(experiment_id) + '.json', 'r') as f:
        tree_data = json.load(f)

    tree_nodes = tree_data['nodes']
    tree_edges = tree_data['edges']
    tree_positions = tree_data['positions']
    tree_root = tree_data['root']
    initial_firefighter_position = tree_data['initial_firefighter_position']

    # Extraer posicion de los bomberos
    firefighter_positions = result['solution']

    # Generar el objeto tree
    tree = Tree(tree_nodes, tree_edges, tree_positions)   

    visualize = TreeVisualizer(tree)



# Graficar y guardar cada paso de un experimento específico
plot_experiment(1, 'dynamic_programming', experiments_data, results_data, save_path_prefix='experiment_1')