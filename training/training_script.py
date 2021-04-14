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

game_env = EONSWrapperEnv(song_file="train.smm", net_efficacy=1)

"""openai_config = {"env_object": game_env, "num_processes": 0, "app_vis": False, 
"seed": None, "runtime": 20, "episodes": 5, "network_filename": "baby_boy", 
"proc_name": "gnp", "app_name": "ratmann_ddr", "output_spike_counts_params":"",
"encoder": {"spikes": {"flip_flop": 2, "max_spikes": 8, "min": 0, "max": 0.5}}, 
"encoder_interval": 1, "decoder": "wta"}"""

openai_config = {"env_object" : game_env, 
"encoder" : {"spikes" : {"flip_flop" : 2, "max_spikes" : 8, "min" : 0, "max" : 0.5}},
"seed" : None, "encoder_interval" : 1, "decoder" : "wta", 
"runtime" : 50, "episodes" : 10, "network_filename":"testmann", 
"output_spike_counts_params":"", "proc_name":"caspian", "app_name":"ratmann", 
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

eo_params["population_size"] = 10
train_params = {"eons_params": eo_params, "num_epochs": 10}
app.config["show_suites"] = True
score = 0

while score < 100:
	app.train(train_params, gnp.Processor, gnp_params)
	best_net = app.overall_best_net
	score = app.test({"test_seed": 0}, gnp.Processor, gnp_params, best_net)
	print("training round complete. score:", score)

#app.print_network()
