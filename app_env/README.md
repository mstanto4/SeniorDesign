# Rhythm Game Environment

The rhythm game environment is an OpenAI Gym environment that simulates a rhythm game much like *Dance Dance Revolution*. This environment is quite configurable; it allows one to change the length of the track, the note speed, and the thresholds at which different scores are rewarded. These parameters can be customized by passing in a JSON file on environment instantiation.

## The Step Function

Arguably the most important part of this environment is the **step** member function. This function takes as parameters the actions to perform at a given time step of the game, and it returns the resultant state of the game, the reward earned for the action, whether or not the game is finished, and any extraneous information. The **action** parameter is an integer between 0 and 31 (inclusive). This is due to the game accepting five buttons; we simply treated each button as a bit. The **state** parameter is a list containing a number between 0 and 31 (inclusive, showing the note that is coming) and a float between 0 and the track length (inclusive, showing how far away the next note is). The **reward** is determined by the thresholds set on intialization, and **done** is simply a boolean that indicates if the game is done or not. This environment makes no use of the **info** return value, and it is only returned as it is convention in OpenAI Gym environments. In carrying out this process, this function also generates information necessary in visualizing the game for human players.

# EONS Wrapper Environment

In attempting to train networks using EONS on the original environment, it became apparent that the scale of the values returned were too large for EONS to learn in a reasonable amount of time. Thus, in order to keep the original environment in tact for easy visualization and compatibility with other models, a wrapper environment was created that modified the output of a contained rhythm game environment and passed it to EONS.

This environment works by observing the output returned by a base rhythm game environment, and determining if the a note should be played or not. The point at which this is decided is determined by a ``net_efficacy`` parameter passed into the environment on initialization. This environment also functions just like an OpenAI Gym environment. The output state is simply an integer -- either 0 or 1 -- and it takes the same for input. Essentially, it sends a 1 out and hopes to receive a 1 back. The operating model is penalized according the base rhytm game environment if any notes are missed.

This approach sped up EONS training considerably, and it allowed the resultant networks to be transferrable between songs -- a highly desireable trait that was not present when training with the base environment.

# Neuro Utils Modification

In getting EONS to work, a slight modification was made to the OpenAIGymApp class. The ``config`` JSON object now takes an actual environment object in the ``env_object`` parameter rather than a string that names the environment in order to avoid having to register the custom environment with one's local Gym installation.

The ControllApp class was also changed such that the ``test`` member function returns the score achieved by the network in question. Before, there was no feedback from this function.

