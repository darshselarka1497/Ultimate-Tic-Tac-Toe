# ULTIMATE TIC TAC TOE - TEAM 26 B351

Implemented a variation of the famous Tic Tac Toe Game called Ultimate Tic Tac Toe in Python. It consists of nine big tic tac toe boards. Each big board has nine smaller boards with each cell of the board. In the game, players take turn to play in each of the smaller boards until they win the larger board. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing.


### Installing

Install the following python libraries using pip

```
pip install matplotlib
```


### Running the Project

Run GameClientRunner.py to run the project and test out different AI agents against each other or a manual player.

```
python GameClientRunner.py
```


### Instructions

In the terminal, the program gives user an option for assigning player agents to Player 1 and 2 respectively. 

Once that is set, the program then asks the user of the number of times the playing agents should play against each other. *This is Mainly for testing purposes.*

Once all the games are played, it outputs a pie chart of the overall statistics of the playing session with overall wins, losses and draws from performancePlotter.py

The piechart is saved in the working directory as a png file format for future reference.
