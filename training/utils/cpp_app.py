import neuro
from neuro import json as nlohmann
import gym
import numpy as np
import random
import time
import jspace
from neuro import IO_Stream
from .control_app import ControlApp

class CppApp(ControlApp):
    def __init__(self, app, config):
        super().__init__(config)
        self.app = app
        self.app.from_json(config["app_config"])
        self.obs_space = self.app.observation_space().as_json().to_python()
        self.action_space = self.app.action_space().as_json().to_python()

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

            ea_json["dmin"] = self.obs_space["low"]
            ea_json["dmax"] = self.obs_space["high"]
            ea_json["interval"] = config["encoder_interval"]

            self.encoder = neuro.EncoderArray(ea_json)
        
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

            if ("low" in self.action_space.keys()):
                da_json["dmin"] = self.action_space["low"]
                da_json["dmax"] = self.action_space["high"]
            else:
                val = self.action_space["max"]
                da_json["dmin"] = [0]
                da_json["dmax"] = [val-1]

            self.decoder = neuro.DecoderArray(da_json)

        self.n_inputs = self.encoder.get_num_neurons()
        self.n_outputs = self.decoder.get_num_neurons()

    def do_one_episode(self, network, processor, seed):
        self.app.seed(seed)
        if (network is not None):
            processor.load_network(network)
        else:
            processor.clear_activity()

        for i in range(self.n_outputs):
            processor.track_output(i)

        timesteps = 0
        score = 0
        rv, observations = self.app.reset()
        rv = False
        info = nlohmann()
        while (rv == False):
            actions = self.get_actions(processor, observations, timesteps)

            if self.config["printing_params"]["show_actions"]:
                print("Timestep {:4d}.  Actions:".format(timesteps), end=" ")
                for action in actions:
                    print(action, end=" ")
                print()

            timesteps += 1
            rv, observations, reward, info = self.app.step(actions)

            score += reward

            if self.config["printing_params"]["show_observations"]:
                print("Timestep {:4d}.  Observations:".format(timesteps), end=" ")
                for observation in observations:
                    print(observation, end=" ")
                print()
            if self.config["printing_params"]["show_rewards"]:
                print("Timestep: {:3d} Reward: {:f}".format(timesteps, reward))
            if self.config["printing_params"]["show_episodes"]:
                print("Episode seed: {:3d} fitness: {:f}".format(seed, score))
            if self.config["printing_params"]["show_done_info"]:
                print("Episode seed: {:3d} json:".format(seed))
                print(info)

        return score
