import rhythm_game_env
import numpy as np

rg = rhythm_game_env.RhythmGameEnv(song_file="test.smm", diff="Medium")

print("Number of measures:", len(rg.measure_list))
print(rg.bpms)
print(rg.bpm_beats)
print(rg.bpm_steps)

done = False
score = 0
reward = 0
state = []
blank_note = [False for x in range(5)]
action = blank_note

while not done:
	prev_state = state
	done, reward, state = rg.step(action)
	score += reward

	if reward < 0:
		print("Action:", action)
		print("State:", prev_state)
		print("Reward:", reward)

		if action != list(prev_state[0]):
			print("Mismatch detected.")

		print()

	if state[1] <= rg.perfect_threshold:
		action = list(state[0])

	else:
		action = blank_note


"""	print("Current beat:", rg.curr_beat)
	print("Current measure:", rg.curr_measure)
	print("Current BPM:", rg.curr_bpm) 
	print("Current step:", rg.num_steps)
"""
print("Total Score:", score)
print("Done after", rg.num_steps, "steps.")
print("Current beat:", rg.curr_beat)
print("Current measure:", rg.curr_measure)
print("Current note:", rg.curr_note)