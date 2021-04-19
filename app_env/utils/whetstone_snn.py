import neuro
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

class WhetstoneSNN:
    def __init__(self, config, weights, key, proc, old):
        self.proc = proc

        print(len(weights))
        if (old == 0):
            start = 3
            weights = weights[:len(weights)-1]
            self.orig_weights = []
            for i in range(3, len(weights), 3):
                self.orig_weights.append(weights[i])
                self.orig_weights.append(weights[i+1])
        else: 
            start = 2
        #for i in range(len(weights)):
            #print(weights[i])
            self.orig_weights = weights[start:]

        self.preprocessing_weights = weights[0]
        self.preprocessing_biases = weights[1] 

        self.key = key

        self.weights = []
        self.biases = []
        for i in range(start, len(weights), start):
            self.weights.append(weights[i])
            self.biases.append(weights[i+1])

        self.neurons_per_layer = []
        for i in range(0, len(weights), start):
            self.neurons_per_layer.append(len(weights[i]))
        if (old == 1):
            self.neurons_per_layer.append(len(weights[-1]))
        else:
            self.neurons_per_layer.append(len(weights[-2]))
        print(self.neurons_per_layer)   
        self.convert_weights()
        self.setup_network()
        self.proc.load_network(self.net)
        #print(self.net)

    def convert_weights(self): 
        props = self.proc.get_properties()
        max_weight = props.edges["Weight"].max_value
        min_weight = props.edges["Weight"].min_value
        self.min_threshold = props.nodes["Threshold"].min_value
        t = props.edges["Weight"].type
        #print(props.edges["Weight"].type)
        minv = np.min([np.min(self.orig_weights[i]) for i in range(len(self.orig_weights))])
        maxv = np.max([np.max(self.orig_weights[i]) for i in range(len(self.orig_weights))])
        #print(minv, maxv)
        #maxv = np.max([0.5, maxv])
        #self.threshold_scale = ((0.5-minv)/(maxv-minv))*(255)
        #self.threshold_scale = 127
        #print(self.threshold_scale) 
        if (str(t) == "PropertyType.Integer"):
            t = "int"
        else:
            t = "float"
        self.type = t
        self.threshold = max_weight/2.0
        print(min_weight, max_weight)
        print(self.threshold)        
        if (t == "int"):
            self.threshold = int(self.threshold)
            #print("It's an integer")
        #print("Here", self.threshold)
        all_weights = [] 
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                for k in range(len(self.weights[i][j])):
                    all_weights.append(self.weights[i][j][k])
                    #self.weights[i][j][k] = (self.weights[i][j][k]-minv)/(maxv-minv)*(max_weight-min_weight)+min_weight
                    self.weights[i][j][k] = self.weights[i][j][k]*max_weight
                    if (self.weights[i][j][k] > max_weight):
                        self.weights[i][j][k] = max_weight
                    elif (self.weights[i][j][k] < min_weight):
                        self.weights[i][j][k] = min_weight
                    if (t == "int"):
                        self.weights[i][j][k] = int(self.weights[i][j][k])
         
         
        for i in range(len(self.biases)):
            for j in range(len(self.biases[i])):
                all_weights.append(self.biases[i][j])
                self.biases[i][j] = self.biases[i][j]*max_weight
                #self.biases[i][j] = (self.biases[i][j]-minv)/(maxv-minv)*(max_weight-min_weight)+min_weight
                if (self.biases[i][j] > max_weight):
                    self.biases[i][j] = max_weight
                elif (self.biases[i][j] < min_weight):
                    self.biases[i][j] = min_weight 
                if (t == "int"):
                    self.biases[i][j] = int(self.biases[i][j])

        #print("Max:", np.max(all_weights))
        #print("Min:", np.min(all_weights))

    def setup_network(self):
        self.net = neuro.Network()
        self.net.set_properties(self.proc.get_properties())

        self.start_outputs = 0

        neurons = []
        neurons.append([])
        #print("Here", self.threshold) 
        # Create neurons
        total = 0
        for i in range(1,len(self.neurons_per_layer)):
            neurons.append([])
            for j in range(self.neurons_per_layer[i]):
                node = self.net.add_node(j+total)
                neurons[i].append(j+total)
                self.net.add_input(j+total)
                self.net.add_output(j+total)
                #print("Bad here", self.threshold)
                node.set("Threshold", self.threshold)
                
            total += self.neurons_per_layer[i]
            if (i != len(self.neurons_per_layer)-1):
                self.start_outputs += self.neurons_per_layer[i] 

        self.total_neurons = total

        # Create synapses 
        total = 0

        for i in range(1,len(self.neurons_per_layer)-1):
            for j in range(self.neurons_per_layer[i]):
                #print(self.weights[i-1])
                for k in range(self.neurons_per_layer[i+1]):
                    w = self.weights[i-1][j][k]
                    if (w != 0):
                        edge = self.net.add_edge(neurons[i][j], neurons[i+1][k])
                    #edge = self.net.add_edge(j+total, k+total+self.neurons_per_layer[i])
                    edge.set("Weight", w)
                    edge.set("Delay", 1)
            total+= self.neurons_per_layer[i]
                
        # Create bias neurons/synapses
        total = 0 

        intermediate_total = self.neurons_per_layer[1]

        bias_id = self.total_neurons
        self.bias_neuron = self.net.add_node(bias_id) 
        self.net.add_input(bias_id)
        self.bias_neuron.set("Threshold", max(self.min_threshold, 0)) 
        for i in range(2, len(self.neurons_per_layer)):
            #print(self.biases[i-2])
            for j in range(self.neurons_per_layer[i]):
                edge = self.net.add_edge(bias_id, neurons[i][j])
                edge.set("Weight", self.biases[i-2][j])
                edge.set("Delay", i-1) 
                
            total += self.neurons_per_layer[i] 
            intermediate_total += self.neurons_per_layer[i]

    def apply_input(self, x):
        input_vals = [0]*self.neurons_per_layer[1]
        
        for i in range(len(self.preprocessing_biases)):
            input_vals[i] = self.preprocessing_biases[i]
         
        for i in range(self.neurons_per_layer[1]):
            for j in range(len(self.preprocessing_weights)):
                input_vals[i] += x[j]*self.preprocessing_weights[j][i]

        spikes = []
        for i in range(len(input_vals)):
            if (input_vals[i] < 0):
                input_vals[i] = 0
            elif (input_vals[i] > 1):
                input_vals[i] = 1
            if (input_vals[i] != 0):
                spike = neuro.Spike(id=i, time=0, value=input_vals[i])
                spikes.append(spike)

        spike = neuro.Spike(id=self.bias_neuron.id, time=0, value=1)
        spikes.append(spike)   

        self.proc.apply_spikes(spikes)

    def get_prediction(self, x):
        self.proc.clear_activity()
        self.apply_input(x)
        self.proc.run(50*len(self.neurons_per_layer))
        
        all_spikes = []
        for i in range(0, self.start_outputs):
            all_spikes.append(self.proc.output_count(i))
        #print(all_spikes)
        output_spikes = []
        
        for i in range(self.start_outputs, self.start_outputs+self.neurons_per_layer[-1]):
            output_spikes.append(self.proc.output_count(i))
        #print(output_spikes)
        val = 2*np.array(output_spikes)-1
        d = np.dot(np.array(val), self.key)
        res = np.exp(d)/sum(np.exp(d))
        #print(res)
        mval = np.max(res)
        #print(np.count_nonzero(res == mval)) 
        #print(res, np.argmax(res))
        return np.argmax(res), res

    def get_predictions(self, X):
        
        #predictions = [self.get_prediction(x) for x in X]
        vectors = []
        predictions = []
        for x in X:
            p, v = self.get_prediction(x)
            vectors.append(v)
            predictions.append(p)

        return predictions, vectors
        
