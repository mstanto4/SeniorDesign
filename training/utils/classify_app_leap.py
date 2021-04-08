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

from leap_ec.individual import Individual
import leap_ec.ops as ops
from leap_ec.real_rep.problems import ScalarProblem
from leap_ec.binary_rep.decoders import BinaryToIntDecoder
from leap_ec.binary_rep.initializers import create_binary_sequence
from leap_ec import util
from leap_ec.context import context
from toolz import pipe
from leap_ec.binary_rep.ops import mutate_bitflip
from leap_ec import probe
import sys


def set_weights(weights, net):
    i = 0
    for e in net.edges():
        edge = net.get_edge(e[0], e[1])
        if (weights[i]-127 == 128):
            edge.set("Weight", 127)
        else:
            edge.set("Weight", weights[i]-127)
        i += 1

    for e in net.edges():
        edge = net.get_edge(e[0], e[1])
        edge.set("Delay", weights[i])
        i+=1

    for n in net.nodes():
        node = net.get_node(n)
        node.set("Threshold", weights[i])
        i+=1
class NetworkProblem(ScalarProblem):
    def __init__(self, net, proc, classify_app):
        super().__init__(maximize=True)
        self.net = net
        self.proc = proc
        self.classify_app = classify_app


    def evaluate(self, weights):
        set_weights(weights, self.net)
        return self.classify_app.get_fitness_score(self.net, self.proc)


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
            split_test_seed = config["app_params"]["split_test_size"]
            split_seed = config["app_params"]["split_seed"]

        self.network_filename = config["network_filename"]
        self.labels = sorted(np.unique(y))
        self.config = config
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=split_test_size, random_state=split_seed)
        
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

        if (temp_net == None):
            if ("eons_seed" in train_config.keys()):
                seed = train_config["eons_seed"]
            else:
                seed = 0
            temp_net = generate_template_network(props, self.n_inputs, self.n_outputs) 
        
        evolver = eons.EONS(train_config["eons_params"])
        evolver.set_template_network(temp_net)

        pop = evolver.generate_population(train_config["eons_params"], 0)
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
                self.overall_best_net.set_data("decoder_array", self.decoder.as_json())
                self.overall_best_net.set_data("other", other)
                self.write_network(self.overall_best_net)
            t1 = time.time()

            #if not self.config["printing_params"]["no_show_epochs"]:
            print("Epoch: {:3d}     Time: {:6.1f}     Best: {}".format(i, t1-t0, overall_best))

            pop = evolver.do_epoch(pop, fitnesses, train_config["eons_params"])

    #TODO: Allow for different accuracy values/custom accuracy values
    #TODO: Add confusion matrix support
    def test(self, test_config, processor, proc_params, net):
        proc = processor(proc_params)
        y_predict = self.predict(proc, net, self.X_train)
        score = accuracy_score(self.y_train, y_predict)
        print("Training Accuracy: ", score)
        print("Training F1 Score: ", f1_score(self.y_train, y_predict, average="weighted"))
        print("Training Confusion Matrix:")
        print(confusion_matrix(self.y_train, y_predict)) 

        y_predict = self.predict(proc, net, self.X_test)
        score = accuracy_score(self.y_test, y_predict)
        print("\nTesting Accuracy: ", score)
        print("Testing F1 Score: ", f1_score(self.y_test, y_predict, average="weighted"))
        print("Testing Confusion Matrix:")
        print(confusion_matrix(self.y_test, y_predict)) 



    def fitness(self, net, proc, id_for_printing=-1):
        total_weights = net.num_edges()
        total_delays = net.num_edges()
        total_thresholds = net.num_nodes()
        dec = [8]*total_weights + [4]*total_delays + [7]*total_thresholds
        leap_decoder = BinaryToIntDecoder(*dec)
        
        problem = NetworkProblem(net, proc, self)
        genome_len = 8*total_weights+4*total_delays+7*total_thresholds
        parents = Individual.create_population(10, initialize=create_binary_sequence(genome_len), decoder=leap_decoder, problem=problem)
        parents = Individual.evaluate_population(parents)
        max_generation = 10
        #stdout_probe = probe.FitnessStatsCSVProbe(context, stream=sys.stdout)
        
        generation_counter = util.inc_generation(context=context)

        while generation_counter.generation() < max_generation:
            offspring = pipe(parents,
                         ops.tournament_selection,
                         ops.clone,
                         mutate_bitflip,
                         ops.uniform_crossover,
                         ops.evaluate,
                         ops.pool(size=len(parents)))#,  # accumulate offspring
                         #stdout_probe)

            parents = offspring
            generation_counter()  # increment to the next generation    
        
        best = probe.best_of_gen(parents).decode()
        set_weights(best, net) 
        return self.get_fitness_score(net, proc, id_for_printing)
        
    def get_fitness_score(self, net, proc, id_for_printing=-1):
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
