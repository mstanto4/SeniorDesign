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

#TODO: Encapsulate all common functionatlies with control into a common utils file
#TODO: Add printing support
#TODO: Add network visualization support
#TODO: Add support for time series data
#TODO: Add native reservoir support

class ClassifyApp():
    def __init__(self, config, X, y):
        split_test_size = config["split_test_size"]
        split_seed = config["split_seed"]
        self.runtime = config["runtime"]


        if ("app_params" not in config.keys()):
            config["app_params"] = {}
            config["app_params"]["split_test_size"] = config["split_test_size"]
            config["app_params"]["split_seed"] = config["split_seed"]
        else:
            split_test_size = config["app_params"]["split_test_size"]
            split_seed = config["app_params"]["split_seed"]

        self.network_filename = config["network_filename"]
        self.labels = sorted(np.unique(y))
        self.config = config
        if (config["split"] == 1):
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=split_test_size, random_state=split_seed)
        else:
            self.X_train = []
            self.y_train = []
            self.X_test = X
            self.y_test = y

        if ("encoder_array" in config.keys()): 
            self.encoder = neuro.EncoderArray(config["encoder_array"]) 
        else:
            ea_json = {}
            if ("encoders" in config.keys()):
                ea_json["encoders"] = config["encoders"]
            elif ("named_encoders" in config.keys()):
                ea_json["named_encoders"] = config["named_encoders"]
                ea_json["use_encoders"] = config["use_encoders"]
            else:
                ea_json["encoders"] = [config["encoder"]]
            
            if (config["timeseries"] == "false"):
                ea_json["dmin"] = [np.min(X[:,i]) for i in range(len(X[0]))]
                ea_json["dmax"] = [np.max(X[:,i]) for i in range(len(X[0]))]
            elif (config["timeseries"] == "true"):
                ea_json["dmin"] = [np.min(X[:,i]) for i in range(len(X[0]))]
                ea_json["dmax"] = [np.max(X[:,i]) for i in range(len(X[0]))]
                
                        

            ea_json["interval"] = config["encoder_interval"]

            self.encoder = neuro.EncoderArray(ea_json)

        # TODO: Encode all of the data as spikes here and store spikes instead of/in addition to data

        # TODO: Allow for multiple outputs scenarios
        if ("decoder_array" in config.keys()):
            self.decoder = neuro.DecoderArray(config["decoder_array"])
        else:
            da_json = {}
            if ("decoders" in config.keys()):
                da_json["decoders"] = config["decoders"]
            elif ("named_decoders" in config.keys()):
                da_json["named_decoders"] = config["named_decoders"]
                da_json["use_decoders"] = config["use_decoders"]
            else:
                da_json["decoders"] = [config["decoder"]]

            da_json["dmin"] = [0]
            da_json["dmax"] = [len(np.unique(y))-1]

            self.decoder = neuro.DecoderArray(da_json) 

        self.n_inputs = self.encoder.get_num_neurons()
        self.n_outputs = self.decoder.get_num_neurons()

    def get_population(self, evolver, train_config, props, temp_net):
        if (temp_net == None):
            if ("eons_seed" in train_config.keys()):
                seed = train_config["eons_seed"]
            else:
                seed = 0
            temp_net = generate_template_network(props, self.n_inputs, self.n_outputs)
        evolver.set_template_network(temp_net)

        pop = evolver.generate_population(train_config["eons_params"], 0)
        return pop

    def train(self, train_config, proc, proc_params, temp_net=None):
        if ("num_processes" not in train_config.keys()):
            pool = Pool()
        elif (train_config["num_processes"] == 0):
            pool = None
        else:
            pool = Pool(train_config["num_processes"])

        other = {}
        other["sim_time"] = self.runtime
        other["proc_name"] = self.config["proc_name"]
        other["app_name"] = self.config["app_name"]

        processor = proc(proc_params)
        props = processor.get_properties()

        self.fitness_type = train_config["fitness"]

        evolver = eons.EONS(train_config["eons_params"])
        pop = self.get_population(evolver, train_config, props, temp_net)
        
        overall_best = -1000000000.0
        self.overall_best_net = None

        num_epochs = train_config["num_epochs"]
        t1 = time.time()
        # TODO: Deal with data passing between processes in the process pool 
        for i in range(num_epochs):
            t0 = t1
            if (pool == None):
                fitnesses = [self.fitness(net.network, processor) for net in pop.networks]
            else:
                bundles = ((self, pop.networks[i].network, proc, proc_params, i) for i in range(len(pop.networks)))
                fitnesses = pool.map(mp_fitness, bundles)
            max_fit = max(fitnesses)
            if (max_fit > overall_best):
                overall_best = max_fit
                self.overall_best_net = pop.networks[np.argmax(fitnesses)].network
                self.overall_best_net.set_data("proc_params", proc_params)
                self.overall_best_net.set_data("app_params", self.config["app_params"])
                self.overall_best_net.set_data("encoder_array", self.encoder.as_json())
                if (self.decoder is not None): self.overall_best_net.set_data("decoder_array", self.decoder.as_json())
                self.overall_best_net.set_data("other", other)
                self.write_network(self.overall_best_net)
            t1 = time.time()

            #if not self.config["printing_params"]["no_show_epochs"]:
            # print("Epoch: {:3d}     Time: {:6.1f}     Best: {}    Num_Synapses: {}".format(i, t1-t0, overall_best, self.overall_best_net.num_edges())) # Commented by MP
            pop = evolver.do_epoch(pop, fitnesses, train_config["eons_params"])

    #TODO: Allow for different accuracy values/custom accuracy values
    #TODO: Add confusion matrix support
    def test(self, test_config, processor, proc_params, net):
        proc = processor(proc_params)
        if (self.config["split"] == 1):
            y_predict = self.predict(proc, net, self.X_train)
            score_train = accuracy_score(self.y_train, y_predict) # modified by MP
            # print("Training Accuracy: ", score_train ) # Commented by MP
            # print("Training F1 Score: ", f1_score(self.y_train, y_predict, average="weighted")) # Commented by MP
            # print("Training Confusion Matrix:")
            # print(confusion_matrix(self.y_train, y_predict)) # Commented by MP

        y_predict = self.predict(proc, net, self.X_test)
        score_test = accuracy_score(self.y_test, y_predict) # modified by MP
        # print("\nTesting Accuracy: ", score_test) # Commented by MP
        # print("Testing F1 Score: ", f1_score(self.y_test, y_predict, average="weighted")) # Commented by MP
        # print("Testing Confusion Matrix:") # Commented by MP
        # print(confusion_matrix(self.y_test, y_predict)) # Commented by MP
        return [score_train, score_test] # added by MP



    def fitness(self, net, proc, id_for_printing=-1):
        y_predict = self.predict(proc, net, self.X_train)
        if (self.fitness_type == "accuracy"):
            ret = accuracy_score(self.y_train, y_predict) 
        elif (self.fitness_type == "f1"):
            ret = f1_score(self.y_train, y_predict, average="weighted")
        return ret
    
    def get_prediction(self, proc, net, x, i=None):
        if (net is not None):
            proc.load_network(net)
        else:
            proc.clear_activity()
    
        for i in range(self.n_outputs):
            proc.track_output(i)
   
        if (self.config["timeseries"] == "false"): 
            spikes = self.encoder.get_spikes(x)
        elif (self.config["timeseries"] == "true"):
            spikes = self.encoder.get_timeseries_spikes(x)
        proc.apply_spikes(spikes)
        
        proc.run(self.runtime)
        label_index = int(self.decoder.get_data_from_processor(proc)[0])
        label = self.labels[label_index]
        
        return label

    def predict(self, proc, net, X):
        proc.load_network(net) 

        return [self.get_prediction(proc, None, x, i) for i, x in enumerate(X)]

    def write_network(self, network, fn=None):
        if (fn == None):
            fn = self.network_filename
        with open(fn, 'w') as f:
            f.write(str(json.dumps(network.as_json().to_python())))
            f.close()

    def read_network(self,fn=None):
        if (fn == None):
            fn = self.network_filename
        with open(fn, 'r') as f:
            s = f.read()
            j = json.loads(s)
            net = neuro.Network()
            net.from_json(j)
        return net

    def from_json(self):
        pass

    def to_json(self):
        pass


def mp_fitness(bundle):
    app, net, proc, proc_name, i = bundle
    processor = proc(proc_name)
    return app.fitness(net, processor, i)
