import neuro
import gym
import numpy as np
import random
import time
import math
import sys
from .control_app import ControlApp

class OpenAIGymApp(ControlApp):
    def __init__(self, config):
        super().__init__(config)
        
        # self.env_name = config["env_name"]
        gym.logger.set_level(40)

        # self.env = gym.make(self.env_name)
        self.env = config["env_object"]

        # Setup encoder
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
  
            self.input_max = [1 if math.isinf(im) else float(im) for im in self.env.observation_space.high]
            self.input_min = [-1 if math.isinf(im) else float(im) for im in self.env.observation_space.low]

            ea_json["dmin"] = self.input_min
            ea_json["dmax"] = self.input_max
            ea_json["interval"] = config["encoder_interval"]

            self.encoder = neuro.EncoderArray(ea_json)
 
        if (isinstance(self.env.action_space, gym.spaces.box.Box)):
            self.box_action = True
            action_min = self.env.action_space.low
            self.action_min = []
            for i in range(len(action_min)):
                self.action_min.append(float(action_min[i]))

            action_max = self.env.action_space.high
            self.action_max = []
            for i in range(len(action_max)):
                self.action_max.append(float(action_max[i]))
            self.actions = 2*self.env.action_space.shape[0]
        else:
            self.box_action = False
            self.action_min = [0]
            self.action_max = [self.env.action_space.n-1]
            self.actions = self.env.action_space.n 

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
                #da_json["decoders"] = []
                #for i in range(len(self.action_min)):
                #    da_json["decoders"].append(config["decoder"])
                da_json["decoders"] = [config["decoder"]]

            da_json["dmin"] = self.action_min
            da_json["dmax"] = self.action_max
            self.decoder = neuro.DecoderArray(da_json)

        self.n_inputs = self.encoder.get_num_neurons()
        self.n_outputs = self.decoder.get_num_neurons()

    def do_one_episode(self, network, processor, seed=None):
        if ("num_processes" not in self.config or self.config["num_processes"] != 0):
            self.env = gym.make(self.env_name)
        if (seed is not None): 
            self.env.seed(seed)
        
        timestep = 0
        if (network is not None):
            processor.load_network()
        else:
            processor.clear_activity()

        for i in range(self.n_outputs):
            processor.track_output(i)
        
        score = 0
        observations = self.env.reset()
        done = False
        while not done:
            t = time.time()
            actions = self.get_actions(processor, observations, timestep)
            timestep += 1
            if (self.box_action == False):
                for i in range(len(actions)):
                    actions[i] = int(actions[i])
            if (len(actions) == 1):
                observations, reward, done, info = self.env.step(actions[0])
            else:
                observations, reward, done, info = self.env.step(actions)
            score += reward
            if (self.config["app_vis"] == True):
                self.env.render()
                while time.time() - t < 0.016: time.sleep(0.001)

        return score 

    def wrap_up(self):
        super().wrap_up()
        self.env.close()
