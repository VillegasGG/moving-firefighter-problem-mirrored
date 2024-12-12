import json
import plotly.graph_objects as go
from fire_simulation import FirePropagation

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

    # Crear graficas de propagacion del fuego y bombero
    fire = FirePropagation(nodes_positions)

    # # Crear la figura base con los nodos
    # fig = go.Figure()

    # # Añadir los nodos
    # for pos in nodes_positions:
    #     fig.add_trace(go.Scatter3d(
    #         x=[pos[0]], y=[pos[1]], z=[pos[2]],
    #         mode='markers',
    #         marker=dict(size=5, color='blue'),
    #         name='Node'
    #     ))

    # # Configurar el layout
    # fig.update_layout(
    #     title=f'Experiment {experiment_id}',
    #     scene=dict(
    #         xaxis_title='X',
    #         yaxis_title='Y',
    #         zaxis_title='Z'
    #     )
    # )

    # # Iterar sobre las posiciones del bombero y guardar cada paso
    # for step, pos in enumerate(firefighter_positions):
    #     if pos != -1:  # Ignorar posiciones no válidas
    #         node_pos = nodes_positions[pos]
    #         fig.add_trace(go.Scatter3d(
    #             x=[node_pos[0]], y=[node_pos[1]], z=[node_pos[2]],
    #             mode='markers',
    #             marker=dict(size=5, color='red'),
    #             name=f'Firefighter Step {step + 1}'
    #         ))

    #         # Mostrar la figura
    #         fig.show()

    #         # Guardar la figura si se proporciona una ruta
    #         if save_path_prefix:
    #             save_path = f"{save_path_prefix}_step_{step + 1}.png"
    #             fig.write_image(save_path)

    #         # Eliminar el último trazo del bombero para el siguiente paso
    #         fig.data = fig.data[:-1]

# Graficar y guardar cada paso de un experimento específico
plot_experiment(1, 'dynamic_programming', experiments_data, results_data, save_path_prefix='experiment_1')