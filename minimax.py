import copy
import numpy as np

class Minimax():
	def __init__(self, depth = 3):
		self.depth = depth
		self.max = 9999
		self.winning_length = 4
		return

	def minimax(self, game, depth):
		if depth == 0 or game.game_end:
			return self.evaluate(game), 0
		
		best_move = 0
		best_move_value = -self.max

		for move in range(28):
			new_game = copy.deepcopy(game)

			# If the move was illegal, skip it
			if new_game.move(move) == False:
				continue

			move_value, _ = self.minimax(new_game, depth - 1)
			move_value *= -1 # Negamax

			# Free memory
			del new_game

			# Update best move
			if move_value > best_move_value:
				best_move_value = move_value
				best_move = move
		
		return best_move_value, best_move

	# Return evaluation, > 0 if player 1 is winning, otherwise < 0
	def evaluate(self, game):
		def count_consecutive_row(arr):
			changes = np.diff(arr.astype(int), prepend=0, append=0)
			counts = np.where(changes == -1)[0] - np.where(changes == 1)[0]
			return list(counts) if len(counts) > 0 else [0]
		
		# Count consecutive balls on board in straight lines
		def count_consecutive(arr):
			counts = [count_consecutive_row(row_or_col) for row_or_col in arr]
			return [x for xs in counts for x in xs]
		
		def score_consecutive(consecutive_balls):
			if consecutive_balls > 4:
				raise Exception("More than 4 balls in a row.")
			
			scores = {0: 0, 1: 0, 2: 1, 3: 5, 4: 9999} # 3 is worth a lot more than 2
			return scores[consecutive_balls]
		
		def get_diagonals(array):
			diagonals = []
			rows, cols = array.shape

			# Get diagonals from the top-left to the bottom-right
			for k in range(-rows + 4, cols - (4 - 1)):
				diagonals.append(np.diagonal(array, offset=k))

			return diagonals
		
		# early exit on game end
		if game.game_end:
			return self.max * (1 if game.winner == 1 else -1) * (1 if game.turn == 1 else -1)

		players = [1, 2]
		player_scores = {player: 0 for player in players}

		for player in players:
			rows = count_consecutive(np.moveaxis(game.board, 0, 0) == player)
			cols = count_consecutive(np.moveaxis(game.board, 1, 0) == player)

			diag_r = count_consecutive([d == player for d in get_diagonals(game.board)])
			diag_l = count_consecutive([d == player for d in get_diagonals(np.fliplr(game.board))])

			player_scores[player] += (
				sum(map(score_consecutive, rows)) +
				sum(map(score_consecutive, cols)) +
				sum(map(score_consecutive, diag_r)) +
				sum(map(score_consecutive, diag_l))
			)

		return (player_scores[1] - player_scores[2]) * (1 if game.turn == 1 else -1)

	def move(self, game):
		_, move = self.minimax(game, self.depth)
		print(f"Minimax choosing move {move}.")
		return move