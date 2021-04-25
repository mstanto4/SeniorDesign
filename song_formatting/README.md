# Creating New Song Options

Step 1: Go to https://search.stepmaniaonline.net
* Search for song of choice.
* Download the pack with song of choice in it.
* Find folder that includes music file and .sm file for song of choice.

Step 2: Convert .sm file into .smm file using parse.py. 
How to Run:
```
python3 parse.py songFile.sm
```

Step 3: Convert music file into a .wav file if not a .wav file already  

Step 4: Move music file into SeniorDesign/app_env/res/sounds   

Step 5: Move .smm file into SeniorDesign/app_env/res/smmFiles   

Step 6: Change comment line indicating music file in .smm file to .wav   

Step 7: Change file indicated in SeniorDesign/app_env/game_vis.py to point to new .smm file    
