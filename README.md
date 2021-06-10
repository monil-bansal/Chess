

# Chess


![ezgif com-gif-maker](https://user-images.githubusercontent.com/31930832/121518639-589d7880-ca0e-11eb-9dd8-2b06dc1378ee.gif)


### Files : 
  1) ChessMain.py: Contains the code to handle user input and draw the game visuals
  2) ChessEngine.py : Contains the logic of the Chess game (Using Brute Force Algorithm for calculating valid moves)
  3) ChessEngineAd.py :  Contains the logic of the Chess game (Using Optimised Algorithm for calculating valid moves)
  4) ChessBot.py : Contains the logic for the BOT to play smartly considering captures, defences and positional advantages to some extent.

###Library to be installed for this Chess engine to work : 
- pyGame: `pip3 install pygame`

### To play the game using optimised algorithm run  the following command in the terminal :
`python3 ChessMain.py adv` or `python ChessMain.py adv`

### To play the game using brute force algorithm run  the following command in the terminal :
`python3 ChessMain.py` or  `python ChessMain.py`

--------

#### To choose whether to play a 2 player game or vs Computer or just see Computer Playing against itself make the following changes in the Config File:
 
  - For Playing as White (Default)       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     : Set PLAYER_ONE_HUMAN = True and PLAYER_TWO_HUMAN = False
  
  -  For Playing as Black               &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    : Set PLAYER_TWO_HUMAN = True and PLAYER_ONE_HUMAN = False
  - For 2 Player Game                   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      : Set both PLAYER_ONE_HUMAN and PLAYER_TWO_HUMAN = True
  - For seeing Computer play from both sides &nbsp;  : Set both PLAYER_ONE_HUMAN and PLAYER_TWO_HUMAN = False
  
