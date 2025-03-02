import copy
import numpy as np

class Minimax():
	def __init__(self, game, depth = 3):
		self.depth = depth
		self.max = 9999

		self.winning_length = game.winning_length
		self.size = game.size
		return

	def minimax(self, game, depth, full=False):
		if depth == 0 or game.game_end:
			return self.evaluate(game), 0
		
		best_move = None
		best_move_value = -self.max

		# If no full check was requested
		if not full:
			# Choose relevant moves based on simple heuristic
			# This drastically reduces search time for minimax
			moves = self.get_relevant_moves(game)
		else:
			moves = range(self.size * 4)
			
		for move in moves:
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
		
		if best_move is not None:
			return best_move_value, best_move
		else:
			# If there was no legal move, run full search
			return self.minimax(game, depth, full=True)
	
	# Choose relevant moves based on simple heuristic
	# If there is a marble at any point around the insertion point, the move is deemed relevant.
	def get_relevant_moves(self, game):
		relevant_moves = []

		mv = 0
		for side in range(4):
			for i in range(self.size):
				if side == 0:
					r, c = 0, i
				elif side == 1:
					r, c = i, self.size - 1
				elif side == 2:
					r, c = self.size - 1, i
				elif side == 3:
					r, c = i, 0

				if self.check_around(game, r, c):
					relevant_moves += [mv]

				mv += 1

		if len(relevant_moves) == 0:
			# If the bot starts, play move 0
			return [0]
		return list(set(relevant_moves))
	
	# Check if squares around the insertion point are empty
	def check_around(self, game, r, c):
		if game.board[r, c] != 0:
			return True
		if r - 1 >= 0 and game.board[r - 1, c] != 0:
			return True
		if r + 1 < game.size and game.board[r + 1, c] != 0:
			return True
		if c - 1 >= 0 and game.board[r, c - 1] != 0:
			return True
		if c + 1 < game.size and game.board[r, c + 1] != 0:
			return True
		return False

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
			if consecutive_balls > self.winning_length:
				raise Exception(f"More than {self.winning_length} marbles in a row.")
			
			# Square increase in value for length of marble chain
			# 0:0, 1:0, 2:4, 3:9, 5:25
			scores = {i: i**2 if i > 1 else 0 for i in range(self.winning_length)}
			return scores[consecutive_balls]
		
		def get_diagonals(array):
			diagonals = []
			rows, cols = array.shape

			# Get diagonals from the top-left to the bottom-right
			for k in range(-rows + self.winning_length, cols - (self.winning_length - 1)):
				diagonals.append(np.diagonal(array, offset=k))

			return diagonals
		
		# early exit on game end
		if game.game_end:
			return (self.max - 10) * (1 if game.winner == 1 else -1) * (1 if game.turn == 1 else -1)

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
		value, move = self.minimax(game, self.depth)
		#print(f"Minimax chose move {move} (eval: {value}).")
		return move, value