import rhythm_game_env
import numpy as np

rg = rhythm_game_env.RhythmGameEnv(song_file="test.smm", diff="Easy")

print("Number of measures:", len(rg.measure_list))
print(rg.bpms)

done = False
score = 0
reward = 0
state = []
blank_note = [False for x in range(5)]
action = blank_note

while not done:
	done, reward, state = rg.step(action)
	score += reward

	if state[1] <= rg.perfect_threshold:
		action = list(state[0])

	else:
		action = blank_note

print("Total Score:", score)
print("Done after", rg.num_steps, "steps.")
print("Current beat:", rg.curr_beat)