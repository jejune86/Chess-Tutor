# Chess-Tutor

For chess newbies, Chess-tutor can assist you to play chess. Learning by playing the game!

<img src="assets\images_for_readme\screen.png">

## Contents
- [Chess-Tutor](#chess-tutor)
  - [Contents](#contents)
  - [Introduction](#introduction)
  - [Prerequisite](#prerequisite)
  - [How to play](#how-to-play)
    - [Keyboard input](#keyboard-input)
  - [Details](#details)
    - [Board Information](#board-information)
    - [Screen for Inforamtion](#screen-for-inforamtion)
    - [Feedback](#feedback)
    - [Promotion](#promotion)
  - [Example Images](#example-images)
  - [References](#references)
  - [Licence](#licence)
---

## Introduction

Chessgame against AI. It uses python chess and pygame library.

On the right side of screen, it displays win rate of current board ang gives you a feedback about your move.

You can get optimal move by AI by pressing Space bar. If you played wrong, you can undo/redo move.

There are levels of AI difficulty from 0 to 25. If it is too hard or easy, adjust Ai difficulty.


## Prerequisite

You have to install python chess and pygame, komodo engine (chess engine)
(you can use other engines but, you have to change some codes)


1. Library
```sh
pip install chess
pip install pygame
```

2. Download komodo engine
   
    go to this site https://komodochess.com/ and download komodo 14

    unzip it and put it in CHESS-TUTOR FILE

    <img src="assets\images_for_readme\komodo_location.png">

    (If you are not using windows or having problem with it, go `chess_engine.py` and change path)

## How to play 

If you don't know the basic rule of chess [Click Here](https://en.wikipedia.org/wiki/Rules_of_chess)

Run `main.py` to play

**Click your piece and click the other place to move your piece**

### Keyboard input

Q : Quit the game

R : Reset the game

Space bar : Display optimal move

Left Key : Undo move

Right Key : Redo move

Up key : Increase AI difficulty

Down key : Decrease AI difficulty

## Details

### Board Information 


Selected piece : <img src="assets\images_for_readme\selected.png">

Opponent's last move : <img src="assets\images_for_readme\last_move.png">

Optimal move by AI : <img src="assets\images_for_readme\spacebar.png">




On the top and bottom of the board, it shows pieces captured pieces.

<img src="assets\images_for_readme\captured_piece.png">


### Screen for Inforamtion

<img src="assets\images_for_readme\information.png">

It shows AI Difficulty, Win rate on current board, Feedback and cute kitty chess master.

### Feedback
**The kitty master analyses your move and gives you feedback about the move.**

Even if the win rate is increased, the feedback could be bad. Because your opponent can make mistake.

If there's the way you or your opponent can make forced checkmate,
It tells you the number of moves to checkmate.

### Promotion

<img src="assets\images_for_readme\promotion_screen.png">

If your pawn reaches at the end, you can promte your pawn to rock, knight, bishop or queen.
Click one you want.

## Example Images

<img src="assets\images_for_readme\Running_example.png">
<img src="assets\images_for_readme\promotion.png">
<img src="assets\images_for_readme\checkmate.png">

## References
- [Github python-chess](https://github.com/niklasf/python-chess)
- ChatGPT 4.0

## Licence
Chess-Tutor is licensed under the GPL 3 - see the [LICENSE.md](LICENSE.md) file for details.