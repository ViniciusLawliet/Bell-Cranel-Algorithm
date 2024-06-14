# Bell-Cranel-Algorithm
The Bell Cranel Algorithm is a Python tool designed for generating and visualizing multilayer graphs. It offers customizable parameters for nodes, edges, and interlayer connections, facilitating the modeling and visualization of intricate systems such as dungeons, mazes, and networks.

![Multi-Level Mapping Problem](img\map.png)

## Introduction

Multilayer graphs, also referred to as multidimensional graphs, are a type of graph representation where nodes and edges exist across multiple layers or dimensions. This approach enables the modeling of interconnected systems with intricate relationships that extend beyond a single layer.

The Bell Cranel Algorithm utilizes multilayer graphs to generate and map complex structures. By representing various components of the structure across different layers, it provides a comprehensive view of the system, facilitating analysis, visualization, and exploration.

## Key Features

- **Multilayer Graph Generation**: The algorithm generates multilayer graphs representing complex structures with interconnected components.
- **Customizable Parameters**: Users can specify parameters such as the number of layers, minimum and maximum nodes per layer, minimum and maximum edges per layer, and interlayer connections.
- **Inspired by DanMachi**: Inspired by the mapping problem featured in the anime "Is It Wrong to Try to Pick Up Girls in a Dungeon?" (DanMachi), the algorithm aims to address similar mapping challenges encountered in complex environments. [DanMachi Dungeon](https://danmachi.fandom.com/wiki/Dungeon).
- **Mapping Complex Structures**: Ideal for mapping complex systems such as dungeons, mazes, networks, and other intricate structures.
- **Visualization**: Utilizes Plotly library to visualize generated multilayer graphs in a three-dimensional (3D) projection, providing an intuitive representation of the structure.

## Usage

### Parameters

- **num_layers**: Number of layers in the graph.
- **min_nodes_per_layer**: Minimum number of nodes per layer.
- **max_nodes_per_layer**: Maximum number of nodes per layer.
- **min_edges_per_layer**: Minimum number of edges per layer.
- **max_edges_per_layer**: Maximum number of edges per layer.
- **interlayer_edges**: Number of edges connecting nodes between layers.
- **animation_speed**: Speed of the animation in milliseconds per frame.
- **allow_disconnected_nodes**: Whether to allow nodes without any edges.

### Features

- **Toggle Axes Visibility**: Use the "Hide Axes" and "Show Axes" buttons to toggle the visibility of the x, y, and z axes in the 3D plot.
- **Play Animation**: Click the "Play" button to animate the construction of the graph edge by edge.


## Installation

To run this project, you need to have Python and the required libraries installed. You can install the required libraries using the following command:

```sh
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.