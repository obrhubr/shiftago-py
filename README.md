# ShiftagoPy

This project provides a high level API for the game "Shiftago" written in Python. It also includes a minimax solver, written in Python.

### The Game "Shiftago"

![Shiftago game](https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Shiftago_05.jpg/330px-Shiftago_05.jpg)

The rules are availiable under [https://de.wikipedia.org/wiki/Shiftago](https://de.wikipedia.org/wiki/Shiftago). 

TLDR: The game is played on a 7x7 board. The goal of the game is to align 4 pieces vertically, horizontally or diagonally. The players push in their pieces from the side, shifting the whole column or line in the process.

### Usage

Run `main.py` to play against a basic minimax algorithm.

### The implementation

The library provides a `Shiftago` object, which implements the game. Players have to implement the move method, which is called to get their move and passed to the game object, which updates state.

The following moves are possible. Each number corresponds to the direction from which you push in your marble.

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

The game checks for win conditions and updates the `winner` and `gameEnd` attributes.
