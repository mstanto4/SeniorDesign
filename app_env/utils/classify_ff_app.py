import time
import json
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import neuro
from multiprocessing import Pool
import eons
import random
from .common_utils import *
from .classify_app import ClassifyApp

class ClassifyFFApp(ClassifyApp):
    def __init__(self, config, X, y):
        super().__init__(config, X, y)
        self.config["layers"] = config["layers"]

    def get_population(self, evolver, train_config, props, temp_net): 
        layers = [self.n_inputs]
        for i in range(len(self.config["layers"])):
            layers.append(self.config["layers"][i])
        layers.append(self.n_outputs)
        temp_net = make_feed_forward(props, layers)
        evolver.set_template_network(temp_net)

        pop = evolver.generate_population(train_config["eons_params"], 0)
        pop.init_from_network(temp_net, train_config["eons_params"]["population_size"])
        return pop
