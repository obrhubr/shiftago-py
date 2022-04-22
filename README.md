# ShiftagoPy

This project provides a high level API for the game "Shiftago" written in Python. It also includes a minimax solver, written in Python.

### The Game "Shiftago"

![Shiftago game](https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Shiftago_05.jpg/330px-Shiftago_05.jpg)

The rules are availiable under [https://de.wikipedia.org/wiki/Shiftago](https://de.wikipedia.org/wiki/Shiftago). 

TLDR: The game is played on a 7x7 board. The goal of the game is to align 4 pieces vertically, horizontally or diagonally. The players push in their pieces from the side, shifting the whole column or line in the process. There is also an "Extreme Mode". In this mode the goal is to get 10 points as fast as possible. If 4 pieces are aligned, they are removed from the field and 0 points are awarded. If the line is longer however points are awarded.

### Usage

I used this library to implement my AlphaZero AI to play Shiftago: [github.com/obrhubr/alpha-shiftago](https://www.github.com/obrhubr/alpha-shiftago)

### The implementation

The library provides a `SimpleShiftagoGame` and `ExtremeShiftagoGame` object. They implement the corresponding gamemodes. They provides the `move` method. You need to provide a number, corresponding to the spot on which to insert the piece.

```
       0  1  2  3  4  5  6
       _  _  _  _  _  _  _ 
  27 |                     |  7
  26 |                     |  8
  25 |                     |  9
  24 |                     |  10
  23 |                     |  11
  22 |                     |  12
  21 |                     |  13
       _  _  _  _  _  _  _ 
       20 19 18 17 16 15 14

```

It then automatically handles the checking for the win condition and updates the `winner` and `gameEnd` attributes.
