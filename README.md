# RATMANN : Rage Against The Multi-Layer Adaptive Neural Network

This repository is the code for RATMANN, a senior design project for ECE / COSC 401 and 402 at the
University of Tennessee, Knoxville. The sponsor of this project is [TENNLab@UTK](https://neuromorphic.eecs.utk.edu/), 
a laboratory investigating neuromorphic computing.

RATMANN is an arcade-style housing that implements a 2-player game similar to *Dance Dance Revolution*
and *Guitar Hero*. It is a timing based game, where a song plays, and the player has to press one of
5 buttons corresponding to a note that appears on the screen. This game has two players: a human player, 
and a neural network player.

The goal of this project is to use a competitive game with a scoring system to demonstrate the
efficacy and a potential use-case of neural networks. The target audience for this project is 
high school students or college students who have not been exposed to artificial intelligence.
The intent is for this arcade game to be used as a demonstration for tours, conferences, and 
potentially to use as a demo at high schools.

This project is developed using OpenAI Gym. It was developed using a neural network model from
TENNLab called GNP, but it is also compatible with any model that can be used with OpenAI Gym.

The intention is this arcade machine can be repurposed for similar types of game-style applications.

## Repository

The repository holds several sections:

1. `app_env`: app environment for OpenAI Gym, as well as the game visualizer.
2. `firmware`: hardware and housing documentation; code that integrates the game with the arcade
housing and the raspberry pi.
3. `song_formatting`: information and formatting for songs that are used in the game.
4. `neuro_lib`: libraries used for the TENNLab neural network model.
5. `training`: files used to train TENNLab neural networks.


## Setup

To set up and run the game on the arcade machine, perform the following steps:

1. Take of the back, hook up a keyboard and mouse to the pi.
2. Power the pi and monitors.
3. Run the following commands to ensure the pi is up to date:
```
sudo apt update
sudo apt full-upgrade
```
4. Clone this repository.
5. Run the following command from this repo:
```
cp firmware/launcher.sh /home/pi/Desktop
cd /home/pi/Desktop
chmod 755 launcher.sh
```
6. Check that the path of the launcher executable matches the path to the cloned repository
7. Run by double-clicking launcher from the desktop, click "Run from terminal"

The game should appear!

