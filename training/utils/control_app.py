import neuro
import eons
from neuro import IO_Stream
import jspace
from neuro import json as nlohmann
from multiprocessing import Pool
import socket
import numpy as np
import random
import time
import json
from .common_utils import *

class ControlApp():
    def __init__(self, config):
        pass
        # Case 1: open AI gym
        # Case 2: cpp app, microapp structure
        # Case 3: standalone python app

        # All parameters will be setup from config
        # Setup encoder/decoder for the application -- this will have to be application specific
        self.episodes = config["episodes"]
        self.seed = config["seed"]
        self.runtime = config["runtime"]
        self.config = config
        self.network_filename = config["network_filename"]
        self.conn = None
        self.config = config
        if (config["output_spike_counts_params"] != ""):
            if config["output_spike_counts_params"]["source"] == "serve":
                # Infers the socket type to be AF_INET from this address
                # configuration.
                addr = ('localhost', config["output_spike_counts_params"]["port"])

                self.listener = socket.socket()
                self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.listener.bind(addr)
                self.listener.listen()
                self.conn, self.address = self.listener.accept()
            else:
                print("output_spike_counts_params only supports the 'serve' source.")
        else:
            self.spike_output_f = None

    def train(self, train_config, proc, proc_params, temp_net = None):
        # Initialize EONS
        # Set up template network from the existing encoder/decoder
        # Initialize population
        # Train and track
        if ("num_processes" not in train_config.keys()):
            pool = Pool()
        elif (train_config["num_processes"] == 0):
            pool = None
        else:
            pool = Pool(train_config["num_processes"])

        processor = proc(proc_params)
        props = processor.get_properties()

        other = {}
        other["sim_time"] = self.runtime
        other["proc_name"] = self.config["proc_name"]
        other["app_name"] = self.config["app_name"]

        if (temp_net == None):
            if ("eons_seed" in train_config.keys()):
                seed = train_config["eons_seed"]
            else:
                seed = 0
            n_inputs = self.encoder.get_num_neurons()
            n_outputs = self.decoder.get_num_neurons()
            temp_net = generate_template_network(props, n_inputs, n_outputs)

        evolver = eons.EONS(train_config["eons_params"])
        evolver.set_template_network(temp_net)

        pop = evolver.generate_population(train_config["eons_params"], 0)
        overall_best = -1000000000.0
        self.overall_best_net = None

        # Print the population if the user wants.
        if self.config["printing_params"]["show_populations"]:
            pop_json = pop.as_json(self.config["printing_params"]["include_networks"])
            print(pop_json)


        num_epochs = train_config["num_epochs"]
        t1 = time.time()
        for i in range(num_epochs):
            t0 = t1
            if (pool == None):
                fitnesses = [self.do_episode_suite(net.network, processor) for net in pop.networks]
            else:
                bundles = ((self, pop.networks[i].network, proc, proc_params, i) for i in range(len(pop.networks)))
                fitnesses = pool.map(mp_fitness, bundles)
            max_fit = max(fitnesses)
            if (max_fit > overall_best):
                overall_best = max_fit
                self.overall_best_net = pop.networks[np.argmax(fitnesses)].network
                self.overall_best_net.set_data("proc_params", proc_params)
                self.overall_best_net.set_data("app_params", self.config["app_config"]) 
                self.overall_best_net.set_data("encoder_array", self.encoder.as_json())
                self.overall_best_net.set_data("decoder_array", self.decoder.as_json())
                self.overall_best_net.set_data("other", other) 
                self.write_network(self.overall_best_net)
            t1 = time.time()

            if not self.config["printing_params"]["no_show_epochs"]:
                print("Epoch: {:3d}     Time: {:6.1f}     Best: {}".format(i, t1-t0, overall_best))

            pop = evolver.do_epoch(pop, fitnesses, train_config["eons_params"])



    def test(self, test_config, proc, proc_params, net):
        # Read in network
        # Run appropriate episodes based on test configurations
        # Output statistics
        processor = proc(proc_params)
        self.seed = test_config["test_seed"]
        score = self.do_episode_suite(net, processor)
        self.wrap_up()
        return score

    def do_one_episode(self, network, processor, seed=0):
        pass

    def do_episode_suite(self, network, processor, id_for_printing=-1):
        score = 0
        processor.load_network(network)
        if (self.seed == None):
            self.seed = random.randint(0,10000000000)
        for i in range(self.episodes):
            score += self.do_one_episode(None, processor, self.seed+i)
        score /= self.episodes

        if (self.config["printing_params"]["show_suites"] == True):
            if (id_for_printing >= 0):
                print("Suite", "{:3d}:".format(id_for_printing), "Fitness", "{}".format(score))
            else:
                print("Fitness", "{}".format(score))

        return score

    # How many times have you called run on the processor up until this point?
    # Returns actions
    def get_actions(self, processor, observations, timestep):
        # IO STREAM seems to be a little wonky with python.
        io = IO_Stream()
        j = nlohmann({"source":"cout"})
        io.create_output_from_json(j)

        spikes = self.encoder.get_spikes(observations)

        if self.config["printing_params"]["show_input_counts"]:
            counts = [0 for x in range(self.encoder.get_num_neurons())]
            for spike in spikes:
                counts[spike.id] += 1
            message = "Timestep %04d.  I-Spike-C:" % timestep
            print(message, end=" ")
            for count in counts:
                print(count, end=" ")
            print()

        processor.apply_spikes(spikes)

        if self.config["output_spike_counts_params"] != "":
            processor.track_spikes()

        processor.run(self.runtime)

        if self.config["output_spike_counts_params"] != "":
            j = processor.get_spike_counts().to_python()
            s = json.dumps(j) + '\n'   # Formatting for the network viz
            self.conn.send(s.encode()) # Send data over the socket.

        actions = self.decoder.get_data_from_processor(processor)

        '''

        I'll come back to this one.

        # Printing.
        # We need an IO_Stream object.
        io = IO_Stream()
        j = nlohmann({"source":"cout"})
        io.create_output_from_json(j)
        times = []
        self.decoder.get_output_counts_and_times(counts, times, processor)
        print(counts, times)

        if self.config["printing_params"]["show_output_counts"]:
            message = "Timestep: %4d 0-Spike-C:" % (timestep)
            io.write_line(message)
        if self.config["printing_params"]["show_output_times"]:
            print("Nah")
        '''
        if self.config["printing_params"]["show_output_counts"]:
            message = "show_output_counts placeholder"
            io.write_line(message)
        if self.config["printing_params"]["show_output_times"]:
            message = "show_output_times placeholder"
            io.write_line(message)

        return actions

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

    def wrap_up(self):
        if (self.conn is not None):
            self.conn.close()
            self.listener.close()

def mp_fitness(bundle):
    app, net, proc, proc_name, i = bundle
    processor = proc(proc_name)
    return app.do_episode_suite(net, processor, i)
