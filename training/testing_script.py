""" Configurable script for testing networks in the EONSWrapper environment. """

import argparse
import neuro
import gnp
import gym
import json
import sys
from utils.openai_gym import *
from eons_wrap_env import EONSWrapperEnv

parser = argparse.ArgumentParser(description="RATMANN Testing Script")
parser.add_argument("--params_file", required=False, type=str, default=None)
parser.add_argument("--song_file", required=False, type=str, default="test.smm")
parser.add_argument("--network_filename", required=False, type=str, default="network.json")
parser.add_argument("--difficulty", required=False, type=str, default="Easy")
parser.add_argument("--network_efficacy", required=False, type=int, default=3)
args = parser.parse_args()

game_env = EONSWrapperEnv(params_file=args.params_file, song_file=args.song_file, diff=args.difficulty, net_efficacy=args.network_efficacy)

openai_config = {"env_object" : game_env, 
"encoder" : {"spikes" : {"flip_flop" : 2, "max_spikes" : 8, "min" : 0, "max" : 0.5}},
"seed" : None, "encoder_interval" : 1, "decoder" : "wta", 
"runtime" : 20, "episodes" : 10, "network_filename":"testmann", 
"output_spike_counts_params":"", "proc_name":"gnp", "app_name":"ratmann", 
"printing_params" : {"show_populations": False, "include_networks": True, 
"show_input_counts": False, "show_output_counts": False, "show_output_times": False, 
"show_suites": False, "no_show_epochs": False}, "app_vis": False, "app_config": {}}

app = OpenAIGymApp(openai_config)

with open("config/gnp.json") as f:
	gnp_params = json.loads(f.read())

proc = gnp.Processor(gnp_params)
net = app.read_network(args.network_filename)
score = app.test({"test_seed": 0}, gnp.Processor, gnp_params, net)
print(score)
