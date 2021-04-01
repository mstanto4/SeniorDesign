import neuro
import gnp
import gym
import json
import sys
from utils.openai_gym import *

# Temporary solution to gaining access to env
sys.path.append('..')
from app_env.rhythm_game_env import *

game_env = RhythmGameEnv(song_file="test.smm")

openai_config = {"env_object": game_env, "num_processes": 0, "app_vis": False, 
"seed": None, "runtime": 20, "episodes": 5, "network_filename": "baby_boy", 
"proc_name": "gnp", "app_name": "ratmann_ddr", "output_spike_counts_params":"",
"encoder": {"spikes": {"flip_flop": 2, "max_spikes": 8, "min": 0, "max": 0.5}}}

app = OpenAIGymApp(openai_config)
