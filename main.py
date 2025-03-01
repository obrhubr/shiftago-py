from shiftagopy import Shiftago
from minimax import Minimax
from human import Human

def play(game, player1, player2):
	print("Starting game: ")
	print(game.board_to_string())

	while not game.game_end:
		# Get player or minimax move
		if game.turn == 1:
			move = player1.move(game)
		else:
			move = player2.move(game)

		# Detect illegal moves
		if not game.move(move):
			print(f"Illegal move!")
			continue

		print(game.board_to_string(highlight_move=move))

	# Game Ended
	print(f"Final state :")
	print(game.board_to_string())
	print(f"Game ended, player {game.winner} won.")
	return

if __name__ == "__main__":
	game = Shiftago(winning_length=5)

	human = Human()
	minimax = Minimax(game, depth=4)

	play(game, human, human)