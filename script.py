import networkx as nx
import plotly.graph_objs as go
import plotly.offline as pyo
import random

# Graph parameters
num_layers = 5
min_nodes_per_layer = 4
max_nodes_per_layer = 10
min_edges_per_layer = 5
max_edges_per_layer = 14
interlayer_edges = 3
animation_speed = 100  # Milliseconds per frame
allow_disconnected_nodes = False

def generate_layer_graph(min_nodes, max_nodes, min_edges, max_edges, allow_disconnected_nodes):
    """
    Generate a single layer graph with given parameters.
    
    Parameters:
    min_nodes (int): Minimum number of nodes in the layer.
    max_nodes (int): Maximum number of nodes in the layer.
    min_edges (int): Minimum number of edges in the layer.
    max_edges (int): Maximum number of edges in the layer.
    allow_disconnected_nodes (bool): Whether to allow disconnected nodes.
    
    Returns:
    G (networkx.Graph): Generated graph for the layer.
    """
    while True:
        num_nodes = random.randint(min_nodes, max_nodes)
        num_edges = random.randint(min_edges, max_edges)
        G = nx.gnm_random_graph(num_nodes, num_edges)
        if allow_disconnected_nodes or all([degree > 0 for _, degree in G.degree()]):
            return G

def connect_layers(G, nodes_G1, nodes_G2, num_edges, edge_list):
    """
    Connect nodes between two layers with given number of edges.
    
    Parameters:
    G (networkx.Graph): The main graph.
    nodes_G1 (list): List of nodes in the first layer.
    nodes_G2 (list): List of nodes in the second layer.
    num_edges (int): Number of edges to connect between layers.
    edge_list (list): List to store edges.
    """
    for _ in range(num_edges):
        u = random.choice(nodes_G1)
        v = random.choice(nodes_G2)
        G.add_edge(u, v)
        edge_list.append((u, v))

def generate_multilayer_graph(num_layers, min_nodes, max_nodes, min_edges, max_edges, interlayer_edges, allow_disconnected_nodes):
    """
    Generate a multilayer graph with given parameters.
    
    Parameters:
    num_layers (int): Number of layers.
    min_nodes (int): Minimum number of nodes per layer.
    max_nodes (int): Maximum number of nodes per layer.
    min_edges (int): Minimum number of edges per layer.
    max_edges (int): Maximum number of edges per layer.
    interlayer_edges (int): Number of edges connecting nodes between layers.
    allow_disconnected_nodes (bool): Whether to allow disconnected nodes.
    
    Returns:
    G (networkx.Graph): Generated multilayer graph.
    pos (dict): Positions of nodes.
    all_edges (list): List of all edges.
    """
    layers = []
    pos = {}
    z_offset = 0
    total_nodes = 0
    all_edges = []

    for _ in range(num_layers):
        layer_graph = generate_layer_graph(min_nodes, max_nodes, min_edges, max_edges, allow_disconnected_nodes)
        layers.append(layer_graph)

    G = nx.Graph()

    for i, layer in enumerate(layers):
        offset = total_nodes
        layer_pos = nx.spring_layout(layer, dim=2)
        for node in layer.nodes:
            G.add_node(node + offset)
            pos[node + offset] = (layer_pos[node][0], layer_pos[node][1], z_offset)
        if i > 0:
            connect_layers(G, range(total_nodes - len(layers[i-1]), total_nodes), range(total_nodes, total_nodes + len(layer)), interlayer_edges, all_edges)
        total_nodes += len(layer)
        z_offset += 1  # Fixed z_offset increment

    for i, layer in enumerate(layers):
        offset = sum(len(layers[j]) for j in range(i))
        edges = [(u + offset, v + offset) for u, v in layer.edges]
        G.add_edges_from(edges)
        all_edges.extend(edges)
    
    return G, pos, all_edges

# Generate multilayer graph
G, pos, all_edges = generate_multilayer_graph(
    num_layers, min_nodes_per_layer, max_nodes_per_layer, min_edges_per_layer, max_edges_per_layer, interlayer_edges, allow_disconnected_nodes
)

# Extract node coordinates
x_nodes = [pos[n][0] for n in G.nodes]
y_nodes = [pos[n][1] for n in G.nodes]
z_nodes = [pos[n][2] for n in G.nodes]

# Trace for nodes
trace_nodes = go.Scatter3d(
    x=x_nodes, y=y_nodes, z=z_nodes, mode='markers',
    marker=dict(size=5, color='blue')
)

# Extract edge coordinates
x_edges = []
y_edges = []
z_edges = []
for edge in all_edges:
    x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
    y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]
    z_edges += [pos[edge[0]][2], pos[edge[1]][2], None]

# Trace for edges
trace_edges = go.Scatter3d(
    x=x_edges, y=y_edges, z=z_edges, mode='lines',
    line=dict(width=2, color='black')
)

# Function to toggle axis visibility
def toggle_axes_visibility(fig, show_axes):
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=show_axes),
            yaxis=dict(visible=show_axes),
            zaxis=dict(visible=show_axes)
        )
    )

# Create layout
layout = go.Layout(
    showlegend=False,
    updatemenus=[
        {
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': animation_speed, 'redraw': True}, 'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [dict(scene=dict(
                        xaxis=dict(visible=False),
                        yaxis=dict(visible=False),
                        zaxis=dict(visible=False)
                    ))],
                    'label': 'Hide Axes',
                    'method': 'relayout'
                },
                {
                    'args': [dict(scene=dict(
                        xaxis=dict(visible=True),
                        yaxis=dict(visible=True),
                        zaxis=dict(visible=True)
                    ))],
                    'label': 'Show Axes',
                    'method': 'relayout'
                }
            ],
            'type': 'buttons',
            'x': 0.1,
            'y': 0,
            'xanchor': 'right',
            'yanchor': 'bottom'
        }
    ]
)

# Create animation frames
frames = []

for i in range(len(all_edges) + 1):
    trace_edges_frame = go.Scatter3d(
        x=x_edges[:i*3], y=y_edges[:i*3], z=z_edges[:i*3], mode='lines',
        line=dict(width=2, color='black')
    )
    
    frame = go.Frame(data=[trace_nodes, trace_edges_frame])
    frames.append(frame)

# Create figure with animation frames
fig = go.Figure(data=[trace_nodes, trace_edges], layout=layout, frames=frames)

# Add initial data to the first frame
fig.frames[0].data = [trace_nodes, trace_edges]

# Display the figure
pyo.plot(fig, filename='multilayer_graph.html', auto_play=False)