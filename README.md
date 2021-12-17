# Hasami Shogi

The board game Hasami Shogi coded in python, utilizing pygame for the GUI.
For this project, the rules of the game follow the rules for Variant 1, as described on 
[the Wikipedia page](https://en.wikipedia.org/wiki/Hasami_shogi). The game is won by capturing
all or all but one of the opponents pieces. 

## Description

This project was created by expanding on a project that was required for a computer science class at OSU.
The original project was purely text based, required printing the game board to the console to play, and did not 
use pygame.
Object oriented programming concepts were utilized to make the code more modularized and to manage data.
A recursive algorithm was implemented to check for pieces to capture after each move.
The GUI was created with the pygame libary and fundamental concepts of game development were implemented to create 
the main game loop. 

### Setup/Installation

You need `python3` to run this game

The project depends on the `pygame` library, install it with pip:
`python3 -m pip install -U pygame --user`

### How to run

You can run the game from the command line, using the following command:
```
python3 main.py
```