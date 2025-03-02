import torch
import copy
import math
import numpy as np
from tqdm import tqdm

from shiftagopy import Shiftago
from minimax import Minimax

def play(game, player1, player2):
	positions, valuations = [], []

	print("Starting game.")
	while not game.game_end:
		# Get player or minimax move
		if game.turn == 1:
			move, value = player1.move(game)
		else:
			move, value = player2.move(game)

		# If the eval becomes too unbalances, cancel
		if abs(value) > 150:
			break

		# Copy board before applying move
		pre_board = copy.deepcopy(game.board)

		# Detect illegal moves
		if not game.move(move):
			continue

		positions += [pre_board]
		valuations += [value]

	# Game Ended
	print(f"Game ended, player {game.winner} won - {game.turn_number} turns.")
	return positions, valuations

def convert_board_to_input(board):
	ones = (board == 1).flatten()
	twos = (board == 2).flatten()
	return np.concatenate((ones, twos)).astype(int)

def normalise(output):
	def sigmoid(x, k=0.01):
		return 2 / (1 + math.exp(-k * x)) - 1
	
	output = np.clip(output, -100, 100)
	return sigmoid(output, k=0.2)

def augment_data(positions, valuations):
	augmented_positions = []

	for p in positions:
		rot1 = np.rot90(p)
		rot2 = np.rot90(rot1)
		augmented_positions += [
			p,
			rot1,
			rot2,
			np.rot90(rot2)
		]

	augmented_valuations = np.array([[v] * 4 for v in valuations]).flatten()

	return augmented_positions, augmented_valuations

if __name__ == "__main__":
	positions, valuations = [], []

	for j in range(49):
		for i in range(16):
			game = Shiftago(winning_length=5)

			# Create random initial play
			game.board[i // 4, i % 4] = 1

			if j == 0:
				continue
			else:
				game.board[j // 7, j % 7] = 2

			minimax = Minimax(game, depth=4)
			ps, vs = play(game, minimax, minimax)

			positions += ps
			valuations += vs

	# Normalise
	valuations = np.array(list(map(lambda v: normalise(v), valuations)))
	# Augment
	positions, valuations = augment_data(positions, valuations)
	# Convert boards to nn input
	positions = np.array(list(map(lambda p: convert_board_to_input(p), positions)))

	# Save move and evaluation
	torch.save(
		(
			torch.tensor(positions).float(), 
			torch.tensor(valuations.reshape((valuations.size, 1))).float()
		),
		"./data/positions.pt"
	)