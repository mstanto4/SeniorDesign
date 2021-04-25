#for including gym / probably wont need or will need to change on pi
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
sys.path.append('../firmware')

cheese0 = 175
cheese1 = 315
cheese2 = 450
cheese3 = 580
cheese4 = 725

import button_func as bf
import rhythm_game_env
import numpy as np
import pyglet as pyg
from pyglet.window import key
from pyglet import font
import random
#from eons_wrap_env import EONSWrapperEnv
#from utils.openai_gym import *
#import gnp
#import gym
#import json
#import neuro

class GameState():
    def __init__(self):	
        self.start = False
        self.gameOver = False
        self.score = 0
        self.reward = 0
        self.state = []
        self.blank_note = [False for x in range(5)]
        self.action = self.blank_note
        self.net_actions_array = self.blank_note
        pyg.resource.add_font('Haster.ttf')
        haster = font.load('HASTER')
        self.scoreText = pyg.text.Label('Score: 0', font_name='HASTER',font_size=48, x=775, y=700)
        self.netScoreText = pyg.text.Label('Neural Score: 0', font_name='HASTER',font_size=48, x=400, y=700)
        self.LEDcounter = [0,0,0,0,0,0,0,0,0,0]

    def update(self, dt):
        if(self.start == False):
            self.action = bf.read_button()
            if(self.action[0] == True):
                self.reset()
                self.rg = rhythm_game_env.RhythmGameEnv(song_file="res/smmFiles/Every.smm", diff="Easy")
 #               self.net_env = EONSWrapperEnv(song_file="res/smmFiles/Every.smm", diff="Easy", net_efficacy=2)
                source = pyg.resource.media(self.rg.music)
                player.queue(source)
                player.volume = 0.1
                player.play()
                self.start = True
            if(self.action[1] == True):
                self.reset()
                self.rg = rhythm_game_env.RhythmGameEnv(song_file="res/smmFiles/Holding Out For A Hero.smm", diff="Easy")
#		self.net_env = EONSWrapperEnv(song_file="res/smmFiles/Holding Out For A Hero.smm", diff="Easy", net_efficacy=2)
                source = pyg.resource.media(self.rg.music)
                player.queue(source)
                player.volume = 0.1
                player.play()
                self.start = True
            if(self.action[2] == True):
                self.reset()
                self.rg = rhythm_game_env.RhythmGameEnv(song_file="res/smmFiles/Bohemian Rhapsody.smm", diff="Hard")
#		self.net_env = EONSWrapperEnv(song_file="res/smmFiles/Bohemian Rhapsody.smm", diff="Hard", net_efficacy=2)
                source = pyg.resource.media(self.rg.music)
                player.queue(source)
                player.volume = 0.1
                player.play()
                self.start = True
            if(self.action[3] == True):
                self.reset()
                self.rg = rhythm_game_env.RhythmGameEnv(song_file="res/smmFiles/mulan.smm", diff="Challenge")
#		self.net_env = EONSWrapperEnv(song_file="res/smmFiles/mulan.smm", diff="Challenge", net_efficacy=2)
                source = pyg.resource.media(self.rg.music)
                player.queue(source)
                player.volume = 0.1
                player.play()
                self.start = True
            if(self.action[4] == True):
                self.reset()
                self.rg = rhythm_game_env.RhythmGameEnv(song_file="res/smmFiles/Georgia.smm", diff="Easy")
#		self.net_env = EONSWrapperEnv(song_file="res/smmFiles/Georgia.smm", diff="Easy", net_efficacy=2)
                source = pyg.resource.media(self.rg.music)
                player.queue(source)
                player.volume = 0.1
                player.play()
                self.start = True
#	    if self.net_env is not None:
                # Set up network player.
#		openai_config = {"env_object" : self.net_env,
#		"encoder" : {"spikes" : {"flip_flop" : 2, "max_spikes" : 8, "min" : 0, "max" : 0.5}},
#		"seed" : None, "encoder_interval" : 1, "decoder" : "wta",
#		"runtime" : 20, "episodes" : 10, "network_filename":"testmann",
#		"output_spike_counts_params":"", "proc_name":"gnp", "app_name":"ratmann",
#		"printing_params" : {"show_populations": False, "include_networks": True,
#		"show_input_counts": False, "show_output_counts": False, "show_output_times": False,
#		"show_suites": False, "no_show_epochs": True}, "app_vis": False, "app_config": {}}

#		self.neuro_app = OpenAIGymApp(openai_config)
#		self.network = self.neuro_app.read_network("ratmann_network.json")
#		self.timestep = 0
#		self.net_score = 0
#		self.net_observations = self.net_env.reset()
#		self.net_done = False

#		with open("config/gnp.json") as f:
#		    gnp_params = json.loads(f.read())

#		self.neuro_proc = gnp.Processor(gnp_params)
#		self.neuro_proc.load_network(self.network)

#		for i in range(self.neuro_app.n_outputs):
#		    self.neuro_proc.track_output(i)
        else:	
            #button stuff
            self.action = bf.read_button()
            if(self.action[0] == True):
                press[0] = 1
                bf.flash_led(bf.LED_P_R, True)
                self.LEDcounter[0] = 10
            else:
                press[0] = 0
            if(self.action[1] == True):
                press[1] = 1
                bf.flash_led(bf.LED_P_Y, True)
                self.LEDcounter[1] = 10
            else:
                press[1] = 0
            if(self.action[2] == True):
                press[2] = 1
                bf.flash_led(bf.LED_P_G, True)
                self.LEDcounter[2] = 10
            else:
                press[2] = 0
            if(self.action[3] == True):
                press[3] = 1
                bf.flash_led(bf.LED_P_B, True)
                self.LEDcounter[3] = 10
            else:
                press[3] = 0
            if(self.action[4] == True):
                press[4] = 1
                bf.flash_led(bf.LED_P_W, True)
                self.LEDcounter[4] = 10
            else:
                press[4] = 0
            
#	    t = time.time()
            action = sum(2**i for i, v in enumerate(reversed(self.action)) if v)

            self.state, self.reward, self.gameOver, info  = self.rg.step(action)
            if self.reward == -1:
                self.score += self.reward
            self.action = [False for x in range(5)]

	    ##### Comment out once neural network works #######
	    ##################################################
            rand = random.randint(0,250)
            if(rand == 23):
                self.net_actions_array[0] = True
            else:
                self.net_actions_array[0] = False
            rand = random.randint(0,250)
            if(rand == 17):
                self.net_actions_array[1] = True
            else:
                self.net_actions_array[1] = False
            rand = random.randint(0,250)
            if(rand == 54):
                self.net_actions_array[2] = True
            else:
                self.net_actions_array[2] = False
            rand = random.randint(0,250)
            if(rand == 91):
                self.net_actions_array[3] = True
            else:
                self.net_actions_array[3] = False
            rand = random.randint(0,250)
            if(rand == 82):
                self.net_actions_array[4] = True
            else:
                self.net_actions_array[4] = False

#	    self.net_actions = self.neuro_app.get_actions(self.neuro_proc, self.net_observations, self.timestep)
#	    self.timestep += 1

#	    if not self.neuro_app.box_action:
#		for i in range(len(self.net_actions)):
#		    self.net_actions[i] = int(self.net_actions[i])

#	    if len(self.net_actions) == 1:
#		self.net_observations, reward, self.net_done, info = self.net_env.step(self.net_actions[0])
#	    else:
#		self.net_observations, reward, self.net_done, info = self.net_env.step(self.net_actions)

#	    self.net_score += reward
#	    self.net_actions_array = [bool((self.net_env.saved_note >> i) & 1) for i in range(4, -1, -1)]

            if(self.net_actions_array[0] == True):
                bf.flash_led(bf.LED_C_R, True)
                self.LEDcounter[5] = 10
            if(self.net_actions_array[1] == True):
                bf.flash_led(bf.LED_C_Y, True)
                self.LEDcounter[6] = 10
            if(self.net_actions_array[2] == True):
                bf.flash_led(bf.LED_C_G, True)
                self.LEDcounter[7] = 10
            if(self.net_actions_array[3] == True):
                bf.flash_led(bf.LED_C_B, True)
                self.LEDcounter[8] = 10
            if(self.net_actions_array[4] == True):
                bf.flash_led(bf.LED_C_W, True)
                self.LEDcounter[9] = 10

            if(len(notes1) != 0):
                for x in range(0, len(notes1)):
                    del notes1[0];
            if(len(notes2) != 0):
                for x in range(0, len(notes2)):
                    del notes2[0];
            if(len(notes3) != 0):
                for x in range(0, len(notes3)):
                    del notes3[0];
            if(len(notes4) != 0):
                for x in range(0, len(notes4)):
                    del notes4[0];
            if(len(notes5) != 0):
                for x in range(0, len(notes5)):
                    del notes5[0];

            for num, note in enumerate(self.rg.visible_notes):
                if(note[0] == True):
                    notes1.append(pyg.sprite.Sprite(note_image, x = cheese0, y = 350 - 1.66*(192 - self.rg.visible_note_distances[num]), batch=note_batch))
                if(note[1] == True):
                    notes2.append(pyg.sprite.Sprite(note_image, x = cheese1, y = 350 - 1.66*(192 - self.rg.visible_note_distances[num]), batch=note_batch))
                if(note[2] == True):
                    notes3.append(pyg.sprite.Sprite(note_image, x = cheese2, y = 350 - 1.66*(192 - self.rg.visible_note_distances[num]), batch=note_batch))
                if(note[3] == True):
                    notes4.append(pyg.sprite.Sprite(note_image, x = cheese3, y = 350 - 1.66*(192 - self.rg.visible_note_distances[num]), batch=note_batch))
                if(note[4] == True):
                    notes5.append(pyg.sprite.Sprite(note_image, x = cheese4, y = 350 - 1.66*(192 - self.rg.visible_note_distances[num]), batch=note_batch))

            self.scoreText.text = "Score: %d" % self.score
#	    self.netScoreText.text = "Neural Score: %d" % self.net_score

            self.LEDcounter[0] = self.LEDcounter[0] - 1
            if(self.LEDcounter[0] == 0):
                bf.flash_led(bf.LED_P_R, False)
            self.LEDcounter[1] = self.LEDcounter[1] - 1
            if(self.LEDcounter[1] == 0):
                bf.flash_led(bf.LED_P_Y, False)		    
            self.LEDcounter[2] = self.LEDcounter[2] - 1
            if(self.LEDcounter[2] == 0):
                bf.flash_led(bf.LED_P_G, False)			
            self.LEDcounter[3] = self.LEDcounter[3] - 1
            if(self.LEDcounter[3] == 0):
                bf.flash_led(bf.LED_P_B, False)			
            self.LEDcounter[4] = self.LEDcounter[4] - 1
            if(self.LEDcounter[4] == 0):
                bf.flash_led(bf.LED_P_W, False)			
            self.LEDcounter[5] = self.LEDcounter[5] - 1
            if(self.LEDcounter[5] == 0):
                bf.flash_led(bf.LED_C_R, False)		    
            self.LEDcounter[6] = self.LEDcounter[6] - 1
            if(self.LEDcounter[6] == 0):
                bf.flash_led(bf.LED_C_Y, False)			
            self.LEDcounter[7] = self.LEDcounter[7] - 1
            if(self.LEDcounter[7] == 0):
                bf.flash_led(bf.LED_C_G, False)			
            self.LEDcounter[8] = self.LEDcounter[8] - 1
            if(self.LEDcounter[8] == 0):
                bf.flash_led(bf.LED_C_B, False)			
            self.LEDcounter[9] = self.LEDcounter[9] - 1
            if(self.LEDcounter[9] == 0):
                bf.flash_led(bf.LED_C_W, False)			

            if(self.gameOver == True):
                self.start = False
#		self.net_env = None

    def reset(self):
        self.start = False
        self.gameOver = False
        self.score = 0
        self.reward = 0
        self.state = []
        self.blank_note = [False for x in range(5)]
        self.action = self.blank_note
        self.net_actions_array = self.blank_note
        self.scoreText = pyg.text.Label('Score: 0', font_name='HASTER',font_size=48, x=775, y=700)
        self.netScoreText = pyg.text.Label('Neural Score: 0', font_name='HASTER',font_size=48, x=400, y=700)
        self.LEDcounter = [0,0,0,0,0,0,0,0,0,0]

pyg.resource.path = ['res','res/images','res/sounds','res/fonts']
pyg.resource.reindex()

#image height = 768 width = 1024
image = pyg.resource.image('BackgroundFinal.png')
window = pyg.window.Window(width = image.width, height = image.height)

pyg.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

@window.event
def update(dt):
    game_state.update(dt)

@window.event
def on_draw():
    window.clear()
    image.blit(0,0)
    note_batch.draw()
    game_state.scoreText.draw()
    if(game_state.start == False and game_state.gameOver == False):
        pop.draw()
        redTextSpice.draw()
        yellowTextSpice.draw()
        greenTextSpice.draw()
        blueTextSpice.draw()
        whiteTextSpice.draw()	
        redText.draw()
        yellowText.draw()
        greenText.draw()
        blueText.draw()
        whiteText.draw()
        RATMANN.draw()
    if(game_state.start == True):
        pressT1.draw()
        pressT2.draw()
        pressT3.draw()
        pressT4.draw()
        pressT5.draw()
        if(press[0] != 0):
            press1.draw()
        if(press[1] != 0):
            press2.draw()
        if(press[2] != 0):
            press3.draw()
        if(press[3] != 0):
            press4.draw()
        if(press[4] != 0):
            press5.draw()
    if(game_state.gameOver == True):
        pop.draw()
        redTextSpice.draw()
        yellowTextSpice.draw()
        greenTextSpice.draw()
        blueTextSpice.draw()
        whiteTextSpice.draw()	
        redText.draw()
        yellowText.draw()
        greenText.draw()
        blueText.draw()
        whiteText.draw()
        if(game_state.score < 100):
            star1.draw()
            starT2.draw()
            starT3.draw()
        if(game_state.score >= 100 and game_state.score <= 300):
            star1.draw()
            star2.draw()
            starT3.draw()
        if(game_state.score > 300):
            star1.draw()
            star2.draw()
            star3.draw()


if __name__ == '__main__':
#setup buttons
    bf.setup()

    game_state = GameState()
    player = pyg.media.Player()

    pyg.resource.path = ['res','res/images','res/sounds','res/fonts']
    pyg.resource.reindex()
    #note height = 70 width = 94

    note_image = pyg.resource.image('testNote.png')
    note_batch = pyg.graphics.Batch()
    notes1 = []
    notes2 = []
    notes3 = []
    notes4 = []
    notes5 = []

    keys = {}
    keys['z'] = False
    keys['x'] = False
    keys['c'] = False
    keys['v'] = False
    keys['b'] = False	
    yellow_image = pyg.resource.image('yellow.png')
    blue_image = pyg.resource.image('blue.png')
    green_image = pyg.resource.image('green.png')
    white_image = pyg.resource.image('white.png')
    red_image = pyg.resource.image('red.png')
    press = [0,0,0,0,0]
    press1 = pyg.sprite.Sprite(red_image, x = cheese0, y = 24)
    press2 = pyg.sprite.Sprite(yellow_image, x = cheese1, y = 24)
    press3 = pyg.sprite.Sprite(green_image, x = cheese2, y = 24)
    press4 = pyg.sprite.Sprite(blue_image, x = cheese3, y = 24)
    press5 = pyg.sprite.Sprite(white_image, x = cheese4, y = 24)

    yellow_image_trans = pyg.resource.image('yellowT.png')
    blue_image_trans = pyg.resource.image('blueT.png')
    green_image_trans = pyg.resource.image('greenT.png')
    white_image_trans = pyg.resource.image('whiteT.png')
    red_image_trans = pyg.resource.image('redT.png')
    pressT1 = pyg.sprite.Sprite(red_image_trans, x = cheese0, y = 24)
    pressT2 = pyg.sprite.Sprite(yellow_image_trans, x = cheese1, y = 24)
    pressT3 = pyg.sprite.Sprite(green_image_trans, x = cheese2, y = 24)
    pressT4 = pyg.sprite.Sprite(blue_image_trans, x = cheese3, y = 24)
    pressT5 = pyg.sprite.Sprite(white_image_trans, x = cheese4, y = 24)

    star_image = pyg.resource.image('star.png')
    star1 = pyg.sprite.Sprite(star_image, x = 350, y = 685)
    star2 = pyg.sprite.Sprite(star_image, x = 450, y = 685)
    star3 = pyg.sprite.Sprite(star_image, x = 550, y = 685)
    star_image_trans = pyg.resource.image('starT.png')
    starT2 = pyg.sprite.Sprite(star_image_trans, x = 450, y = 685)
    starT3 = pyg.sprite.Sprite(star_image_trans, x = 550, y = 685)

    popUp = pyg.resource.image('PopUp2.png')
    pop = pyg.sprite.Sprite(popUp, x = 25, y = 5)

    redText = pyg.text.Label('Press          to play "Everytime I Touch"', font_name='HASTER',font_size=35, x=120, y=600)
    yellowText = pyg.text.Label('Press          to play "Holding Out For A Hero"', font_name='HASTER',font_size=35, x=120, y=500) 
    greenText = pyg.text.Label('Press          to play "Bohemian Rhapsody"', font_name='HASTER',font_size=35, x=120, y=400)
    blueText = pyg.text.Label('Press          to play "I\'ll Make A Man Out Of You"', font_name='HASTER',font_size=35, x=120, y=300)
    whiteText = pyg.text.Label('Press          to play "The Devil Went Down To Georgia"', font_name='HASTER',font_size=35, x=120, y=200)

    RATMANN = pyg.text.Label('RAT MANN',color = [253,150,50,255], font_name = 'HASTER', font_size = 72, x = 10, y = 685)

    redTextSpice = pyg.sprite.Sprite(red_image, x = 200, y = 560)
    yellowTextSpice = pyg.sprite.Sprite(yellow_image, x = 200, y = 460)
    greenTextSpice = pyg.sprite.Sprite(green_image, x = 200, y = 360)
    blueTextSpice = pyg.sprite.Sprite(blue_image, x = 200, y = 260)
    whiteTextSpice = pyg.sprite.Sprite(white_image, x = 200, y = 160)


    pyg.clock.schedule_interval(update, 1/180.0)
    pyg.app.run()
    bf.cleanup()






