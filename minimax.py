import copy
import numpy as np

class Minimax():
	def __init__(self, game, depth = 3):
		self.depth = depth
		self.max = 9999

		self.scoring_rules = {c: c**2 if c > 1 else 0 for c in range(game.winning_length)}

		self.diagonals_rl, self.diagonals_lr = self.generate_diagonals(game.size, game.winning_length)
		return
	
	def generate_diagonals(self, size, winning_length):
		diagonals_rl, diagonals_lr = [], []

		for col in range(size-1, -1, -1):
			x, y = 0, col
			diagonal = []
			while x < size and y < size:
				diagonal.append((x, y))
				x += 1
				y += 1
			if len(diagonal) >= winning_length:
				diagonals_rl += [diagonal]
		for row in range(1, size):
			x, y = row, 0
			diagonal = []
			while x < size and y < size:
				diagonal.append((x, y))
				x += 1
				y += 1
			if len(diagonal) >= winning_length:
				diagonals_rl += [diagonal]

		for col in range(size):
			x, y = 0, col
			diagonal = []
			while x < size and y >= 0:
				diagonal.append((x, y))
				x += 1
				y -= 1
			if len(diagonal) >= winning_length:
				diagonals_lr += [diagonal]
		for row in range(1, size):
			x, y = row, size - 1
			diagonal = []
			while x < size and y >= 0:
				diagonal.append((x, y))
				x += 1
				y -= 1
			if len(diagonal) >= winning_length:
				diagonals_lr += [diagonal]

		return diagonals_rl, diagonals_lr

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
			moves = range(game.size * 4)
			
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
			for i in range(game.size):
				if side == 0:
					r, c = 0, i
				elif side == 1:
					r, c = i, game.size - 1
				elif side == 2:
					r, c = game.size - 1, i
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
		# early exit on game end
		if game.game_end:
			return (self.max - 10) * (1 if game.winner == 1 else -1) * (1 if game.turn == 1 else -1)

		players = [1, 2]
		player_scores = {p: 0 for p in players}

		# Count helpers
		directions = ["r", "c"]
		previous = {d: 0 for d in directions}
		consecutives = {d: 0 for d in directions}

		for idx in range(game.size * game.size):
			r = game.board[idx // game.size, idx % game.size]
			c = game.board[idx % game.size, idx // game.size]

			for current, d in zip([r, c], directions):
				# On col/row change
				if idx % 7 == 0:
					if previous[d] != 0:
						player_scores[previous[d]] += self.scoring_rules[consecutives[d]]

					# Reset
					consecutives[d] = 1
					previous[d] = current
					continue
				
				if current == previous[d]:
					consecutives[d] += 1
				else:
					if previous[d] != 0:
						# Add score to player
						player_scores[previous[d]] += self.scoring_rules[consecutives[d]]
					# Reset consecutive marble count
					consecutives[d] = 1
				# Set previous to current
				previous[d] = current

		directions = ["dr", "dc"]
		previous = {d: 0 for d in directions}
		consecutives = {d: 0 for d in directions}

		for n in range(len(self.diagonals_lr)):
			for idx in range(len(self.diagonals_lr[n])):
				dr = game.board[self.diagonals_lr[n][idx]]
				dc = game.board[self.diagonals_rl[n][idx]]

				for current, d in zip([dr, dc], directions):					
					if current == previous[d]:
						consecutives[d] += 1
					else:
						if previous[d] != 0:
							# Add score to player
							player_scores[previous[d]] += self.scoring_rules[consecutives[d]]
						# Reset consecutive marble count
						consecutives[d] = 1
					# Set previous to current
					previous[d] = current

			for d in directions:
				if previous[d] != 0:
					player_scores[previous[d]] += self.scoring_rules[consecutives[d]]
			# Reset on diagonal change
			previous = {d: 0 for d in directions}
			consecutives = {d: 0 for d in directions}

		return (player_scores[1] - player_scores[2]) * (1 if game.turn == 1 else -1)

	def move(self, game):
		value, move = self.minimax(game, self.depth)

		print(f"Minimax chose move {move} (eval: {value}).")
		return move