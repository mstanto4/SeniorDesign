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
from .classify_app import ClassifyApp

class ReservoirApp(ClassifyApp):
    def __init__(self, config, X, y):


        split_test_size = config["split_test_size"]
        split_seed = config["split_seed"]
        if ("app_params" not in config.keys()):
            config["app_params"] = {}
            config["app_params"]["split_test_size"] = config["split_test_size"]
            config["app_params"]["split_seed"] = config["split_seed"]
        else:
            split_test_size = config["app_params"]["split_test_size"]
            split_seed = config["app_params"]["split_seed"]

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
        self.n_outputs = 20 
        self.decoder = None

    def test(self, test_config, processor, proc_params, net):
        proc = processor(proc_params)
        clf, y_predict = self.train_readout(proc, net)
        proc.load_network(net)
        all_spikes = np.array([self.get_output_spikes(proc, None, x, i) for i, x in enumerate(self.X_test)])
        y_predict = clf.predict(all_spikes)
        score = accuracy_score(self.y_test, y_predict)
        print("Testing Accuracy: ", score)

    def fitness(self, net, proc, id_for_printing=-1):
        clf, y_predict = self.train_readout(proc, net)
        #return accuracy_score(self.y_train, y_predict)
        if (self.fitness_type == "accuracy"):
            ret = accuracy_score(self.y_train, y_predict)
        elif (self.fitness_type == "f1"):
            ret = f1_score(self.y_train, y_predict, average="weighted")
        return ret

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
        return clf, y_predict
