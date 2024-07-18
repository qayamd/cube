# Rubik's Cube Solver

## What is it?
A Python implementation of Monte Carlo Tree Search (MCTS) to train an agent to solve Rubik's Cubes. \
The agent uses parallel processing to explore multiple MCTS trees simultaneously, with a focus on balancing exploration and exploitation.
The idea is that the environment presents the agent with all possible moves, and it chooses the best one based on MCTS results.

## MCTS Architecture
The model used is a Monte Carlo Tree Search, designed to process the state of a Rubik's Cube and decide the best move. The architecture of the MCTS follows:

**Node Structure:**
- Each node represents a Rubik's Cube state and stores visit count and value.

**MCTS Steps:**
- Selection: Choose promising nodes using UCT formula
- Expansion: Add new child nodes to explore new states
- Simulation: Randomly play out the game from the new node
- Backpropagation: Update node statistics based on simulation results

The MCTS was implemented with parallel processing to improve search efficiency. It uses a max depth to limit tree growth and a set number of iterations per move.

## What does what?
* cube.py: Contains the main MCTS implementation and Rubik's Cube solver
* magiccube/: External package for Rubik's Cube representation and manipulation

If you want to run the solver, just execute cube.py. This might take a while, depending on your settings. \
You can adjust parameters like cube size, number of processes, and iterations per move in the main() function.

Thanks to [trincaog](https://pypi.org/user/trincaog/) for the Rubik's Cube implementation.