# Chess-Tutor

For chess newbies, Chess-tutor can assist you to play chess. Learning by playing the game!

<img src="assets\images_for_readme\screen.png">

## Introduction

Chessgame against AI. It uses python chess and pygame library.On the right side of screen, it displays win rate of current board ang gives you a feedback about your move. You can get optimal move by AI by pressing Space bar. If you play wrong, you can undo/redo move. There are 25 levels of AI difficulty. If it is too hard or easy, adjust Ai difficulty.


## Getting Started

You have to install python chess and pygame, komodo engine (chess engine)
(you can use other engines but, you have to change some codes)

### Prerequisites

1. Library
```sh
pip install chess
pip install pygame
```

2. Download komodo engine
   
    go to this site https://komodochess.com/

    and download komodo 14

    unzip it and put it in CHESS-TUTOR FILE

    <img src="assets\images_for_readme\komodo_location.png">

    (if you are not using windows or having problem with it, go chess_engine.py and change path)
## How to play 

If you don't know the basic rule of chess [Click Here](https://en.wikipedia.org/wiki/Rules_of_chess)

Run main.py to play

Click your piece and click the other place to move your piece

keyboard input

Q : Quit the game

R : Reset the game

Space bar : Display optimal move

Left Key : Undo move

Right Key : Redo move

Up key : Increase AI difficulty

Down key : Decrease AI difficulty

## Details

### Board Information 

Each color means below.
Selected piece : <img src="assets\images_for_readme\selected.png">

Opponent's last move : <img src="assets\images_for_readme\last_move.png">

Optimal move by AI : <img src="assets\images_for_readme\spacebar.png">

<img src="assets\images_for_readme\captured_piece.png">
On the top and bottom of board, it shows pieces you and your oppenent capture.

### Screen for Inforamtions

<img src="assets\images_for_readme\informations.png">
It show AI Difficulty, Win rate on current board, Feedback and cute kitty chess master.

### Promotion

<img src="assets\images_for_readme\promotion_screen.png">
If your pawn reaches at the end, you can promte your pawn to rock, knight, bishop or queen.
Click one you want.

## Example Images

<img src="assets\images_for_readme\Running_example.png">
<img src="assets\images_for_readme\promotion.png">
<img src="assets\images_for_readme\checkmate.png">

## Licence
Chess-Tutor is licensed under the GPL 3 - see the [LICENSE.md](LICENSE.md) file for details.