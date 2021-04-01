import time
import json
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
import neuro
from multiprocessing import Pool
import random
from .common_utils import *
import scipy

class StandaloneReservoir():
    def __init__(self, config, X, y):
        split_test_size = config["split_test_size"]
        split_seed = config["split_seed"]
        self.runtime = config["runtime"]
        self.network_filename = config["network_filename"]
        self.labels = sorted(np.unique(y))
        self.config = config
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=split_test_size, random_state=split_seed)

        ea_json = {}
        if ("encoders" in config.keys()):
            ea_json["encoders"] = config["encoders"]
        elif ("named_encoders" in config.keys()):
            ea_json["named_encoders"] = config["named_encoders"]
            ea_json["use_encoders"] = config["use_encoders"]
        else:
            ea_json["encoders"] = [config["encoder"]]

        ea_json["dmin"] = [min(X[:,i]) for i in range(len(X[0]))]
        ea_json["dmax"] = [max(X[:,i]) for i in range(len(X[0]))]

        ea_json["interval"] = config["encoder_interval"]

        self.encoder = neuro.EncoderArray(ea_json)
        self.n_inputs = self.encoder.get_num_neurons()
        self.n_outputs = config["num_outputs"]

    def initialize_network(self, proc, seed, num_hidden, prob_edge):
        properties = proc.get_properties()
        net = neuro.Network()
        net.set_properties(properties)

        moa = neuro.MOA()
        moa.seed(seed)

        for i in range(self.n_inputs):
            node = net.add_node(i)
            net.add_input(i)
            net.randomize_node_properties(moa, node)

        for i in range(self.n_outputs):
            node = net.add_node(i+self.n_inputs)
            net.add_output(i+self.n_inputs)
            net.randomize_node_properties(moa, node)

        total = self.n_inputs+self.n_outputs

        for i in range(num_hidden):
            node = net.add_node(i+total)
            net.randomize_node_properties(moa, node)

        total += num_hidden

        A = scipy.sparse.random(total, total, density=prob_edge, random_state=seed).toarray() 
        for i in range(total):
            for j in range(total):
                if (A[i][j] != 0 and i != j):
                    edge = net.add_edge(i, j)
                    net.randomize_edge_properties(moa, edge)


        return net

    def get_output_spikes(self, proc, net, x, i=None):
        if (net is not None):
            proc.load_network(net)
            for i in range(self.n_outputs):
                proc.track_output(i)
        else:
            proc.clear_activity()


        spikes = self.encoder.get_spikes(x)
        proc.apply_spikes(spikes)

        proc.run(self.runtime)

        out_counts = []
        for i in range(self.n_outputs):
            val = proc.output_count(i)
            out_counts.append(val)
        return out_counts


    def train_readout(self, proc, net):
        proc.load_network(net)
        for i in range(self.n_outputs):
            proc.track_output(i)
        all_spikes = np.array([self.get_output_spikes(proc, None, x, i) for i, x in enumerate(self.X_train)])
        clf = SGDClassifier()
        clf.fit(all_spikes, self.y_train)
        y_predict = clf.predict(all_spikes)
        score = accuracy_score(self.y_train, y_predict)
        # print("Training Accuracy: ", score)
        return [clf,score]

    def test(self, test_config, proc, net, clf=None):
        if (clf == None):
            clf, y_predict = self.train_readout(proc, net)
        proc.load_network(net)
        all_spikes = np.array([self.get_output_spikes(proc, None, x, i) for i, x in enumerate(self.X_test)])
        y_predict = clf.predict(all_spikes)
        score = accuracy_score(self.y_test, y_predict)
        # print("Testing Accuracy: ", score)
        return score

