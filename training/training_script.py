""" Configurable script for training networks to perform in the EONSWrapper environment. """
import argparse
import neuro
import gnp
import caspian
import gym
import json
import sys
from utils.openai_gym import *
from eons_wrap_env import EONSWrapperEnv

# Temporary solution to gaining access to env
sys.path.append('..')
from app_env.rhythm_game_env import *

parser = argparse.ArgumentParser(description="RATMANN Training Script")
parser.add_argument("--params_file", required=False, type=str, default=None)
parser.add_argument("--song_file", required=False, type=str, default="train.smm")
parser.add_argument("--pop_size", required=False, type=int, default=10)
parser.add_argument("--num_epochs", required=False, type=int, default=10)
parser.add_argument("--network_filename", required=False, type=str, default="network.json")
args = parser.parse_args()

game_env = EONSWrapperEnv(params_file=args.params_file, song_file=args.song_file)

"""openai_config = {"env_object": game_env, "num_processes": 0, "app_vis": False, 
"seed": None, "runtime": 20, "episodes": 5, "network_filename": "baby_boy", 
"proc_name": "gnp", "app_name": "ratmann_ddr", "output_spike_counts_params":"",
"encoder": {"spikes": {"flip_flop": 2, "max_spikes": 8, "min": 0, "max": 0.5}}, 
"encoder_interval": 1, "decoder": "wta"}"""

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

with open("config/caspian.json") as f:
	casp_params = json.loads(f.read())

with open("config/eons.json") as f:
	eo_params = json.loads(f.read())

proc = gnp.Processor(gnp_params)

eo_params["population_size"] = args.pop_size
train_params = {"eons_params": eo_params, "num_epochs": args.num_epochs}
app.config["show_suites"] = True
score = 0

while score < 100:
	app.train(train_params, gnp.Processor, gnp_params)
	best_net = app.overall_best_net
	score = app.test({"test_seed": 0}, gnp.Processor, gnp_params, best_net)
	print("training round complete. score:", score)

app.write_network(best_net, args.network_filename)
