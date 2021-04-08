import neuro
import json

def generate_template_network(properties, n_inputs, n_outputs, seed=0):
    net = neuro.Network()
    net.set_properties(properties)
    
    moa = neuro.MOA()
    moa.seed(seed)

    for i in range(n_inputs):
        node = net.add_node(i)
        net.add_input(i)
        net.randomize_node_properties(moa, node)

    for i in range(n_outputs):
        node = net.add_node(i+n_inputs)
        net.add_output(i+n_inputs)
        net.randomize_node_properties(moa, node)

    return net

def read_network(fn):
    with open(fn, 'r') as f:
        s = f.read()
        j = json.loads(s)
        net = neuro.Network()
        net.from_json(j)
    return net

def make_feed_forward(props, layer_size, seed=0):
    moa = neuro.MOA()
    moa.seed(seed)
    net = neuro.Network()
    net.set_properties(props)
    if (len(layer_size) < 2):
        raise ValueError("make_feed_forward requires layers to have at least an input layer and an output layer")

    num_inputs = layer_size[0]
    num_outputs = layer_size[-1]

    layers = []

    layers.append([])
    for i in range(num_inputs):
        node = net.add_node(i)
        net.randomize_node_properties(moa, node)
        net.add_input(i)
        layers[0].append(i)

    current_index = num_inputs+num_outputs

    for i in range(1,len(layer_size)-1):
        layers.append([])
        for j in range(layer_size[i]):
            node = net.add_node(current_index)
            net.randomize_node_properties(moa, node)
            layers[-1].append(current_index)
            current_index += 1

    layers.append([])
    for i in range(num_outputs):
        node = net.add_node(num_inputs+i)
        net.randomize_node_properties(moa, node)
        net.add_output(num_inputs+i)
        layers[-1].append(num_inputs+i)

    for i in range(len(layers)-1):
        for j in range(len(layers[i])):
            for k in range(len(layers[i+1])):
                edge = net.add_edge(layers[i][j], layers[i+1][k])
                net.randomize_edge_properties(moa, edge)
    return net

