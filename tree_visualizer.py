import plotly.graph_objects as go
import pygraphviz as pgv
import numpy as np

class TreeVisualizer:
    def __init__(self, tree):
        self.tree = tree

    def add_edges(self, fig):
        """
        Agregar aristas
        """
        # Graficar aristas
        for i in range(self.tree.edges.shape[0]):
            for j in range(self.tree.edges.shape[1]):
                if self.tree.edges[i, j] == 1:  # Si hay una conexión entre i y j
                    fig.add_trace(go.Scatter3d(
                        x=[self.tree.nodes_positions[i, 0], self.tree.nodes_positions[j, 0]],
                        y=[self.tree.nodes_positions[i, 1], self.tree.nodes_positions[j, 1]],
                        z=[self.tree.nodes_positions[i, 2], self.tree.nodes_positions[j, 2]],
                        mode='lines',
                        line=dict(color='gray', width=2),
                        showlegend=False
                    ))

    def plot_3d_tree(self, tree, img_name):
        """
        Grafica el árbol en 3D con Plotly
        """
        # Crear una figura 3D
        fig = go.Figure()

        # Graficar nodos
        fig.add_trace(go.Scatter3d(
            x=tree.nodes_positions[:, 0],
            y=tree.nodes_positions[:, 1],
            z=tree.nodes_positions[:, 2],
            mode='markers',
            marker=dict(size=10, color='#d2b4de'),
            name='Nodes'
        ))

        self.add_edges(fig)

        firefighter_positions = np.array(tree.get_firefighter_positions())
        if firefighter_positions.size > 0:
            fig.add_trace(go.Scatter3d(
                x=firefighter_positions[:, 0],
                y=firefighter_positions[:, 1],
                z=firefighter_positions[:, 2],
                mode='markers',
                marker=dict(size=10, color='green'),
                name='Firefighters'
            ))

        fig.update_layout(title='3D Tree Structure',
                        scene=dict(
                            xaxis_title='X Axis',
                            yaxis_title='Y Axis',
                            zaxis_title='Z Axis'
                        ),
                        width=700,
                        height=700)

        fig.write_html(img_name + ".html")
    
    def tree_order(self, tree, root):
        """
        Recorre el grafo desde la raiz para su correcta visualizacion
        """
        G = pgv.AGraph()
        adj_matrix = tree.edges

        G.add_node(root)
        stack = [root]
        visitados = set() 

        while stack:
            actual = stack.pop() 
            if actual not in visitados:
                visitados.add(actual) 

                for posicion in range(len(adj_matrix[actual])):
                    if adj_matrix[actual][posicion] == 1: 
                        G.add_node(posicion)
                        G.add_edge(actual, posicion) 
                        
                        if posicion not in visitados:
                            stack.append(posicion) 
        return G

    def plot_2d_tree_with_root(self, tree, root):
        """
        Gráfica del árbol en 2D
        """
        G = self.tree_order(tree, root)
        G.write("pygrapghviz.dot")
        G.layout(prog="dot")
        G.draw("images/grafo_2d_arbol.png")
        G.layout()
        G.draw("images/grafo_2d.png")

    def plot_fire_state(self, burning_nodes, burned_nodes, step):
        """
        Genera y guarda una imagen 3D del estado actual de la propagación del incendio.
        """
        fig = go.Figure()

        # Nodos en llamas (burning)
        fig.add_trace(go.Scatter3d(
            x=[self.tree.nodes_positions[node, 0] for node in burning_nodes],
            y=[self.tree.nodes_positions[node, 1] for node in burning_nodes],
            z=[self.tree.nodes_positions[node, 2] for node in burning_nodes],
            mode='markers',
            marker=dict(size=10, color='red'),
            name='Burning Nodes'
        ))

        # Nodos quemados (burned)
        fig.add_trace(go.Scatter3d(
            x=[self.tree.nodes_positions[node, 0] for node in burned_nodes],
            y=[self.tree.nodes_positions[node, 1] for node in burned_nodes],
            z=[self.tree.nodes_positions[node, 2] for node in burned_nodes],
            mode='markers',
            marker=dict(size=10, color='black'),
            name='Burned Nodes'
        ))

        # Nodos que no han sido quemados ni están en llamas (restantes)
        all_nodes = set(range(self.tree.nodes_positions.shape[0]))
        unaffected_nodes = all_nodes - burning_nodes - burned_nodes

        fig.add_trace(go.Scatter3d(
            x=[self.tree.nodes_positions[node, 0] for node in unaffected_nodes],
            y=[self.tree.nodes_positions[node, 1] for node in unaffected_nodes],
            z=[self.tree.nodes_positions[node, 2] for node in unaffected_nodes],
            mode='markers',
            marker=dict(size=10, color='blue'),
            name='Unaffected Nodes'
        ))

        # Agregar aristas entre nodos
        for i in range(self.tree.edges.shape[0]):
            for j in range(self.tree.edges.shape[1]):
                if self.tree.edges[i, j] == 1:
                    fig.add_trace(go.Scatter3d(
                    x=[self.tree.nodes_positions[i, 0], self.tree.nodes_positions[j, 0]],
                    y=[self.tree.nodes_positions[i, 1], self.tree.nodes_positions[j, 1]],
                    z=[self.tree.nodes_positions[i, 2], self.tree.nodes_positions[j, 2]],
                    mode='lines',
                    line=dict(color='gray', width=2),
                    showlegend=False
                    ))

        # Agregar posiciones de los bomberos
        firefighter_positions = np.array(self.tree.get_firefighter_positions())
        if firefighter_positions.size > 0:
            fig.add_trace(go.Scatter3d(
                x=firefighter_positions[:, 0],
                y=firefighter_positions[:, 1],
                z=firefighter_positions[:, 2],
                mode='markers',
                marker=dict(size=10, color='green'),
                name='Firefighters'
            ))

        # Configuracion
        fig.update_layout(title=f'Step {step}: Fire Propagation',
                        scene=dict(xaxis_title='X Axis', yaxis_title='Y Axis', zaxis_title='Z Axis'),
                        width=700, height=700)

        # Guardar la imagen
        fig.write_image(f"images/steps/step_{step}.png")