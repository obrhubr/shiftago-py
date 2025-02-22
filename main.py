from shiftagopy import Shiftago
from minimax import Minimax
from human import Human

def play(game, player1, player2):
	print("PLAY!")
	game.printBoard()
	print("")

	while not game.gameEnd:
		# Get player or minimax move
		if game.turn:
			move = player1.move(game)
		else:
			move = player2.move(game)

		# Detect illegal moves
		if game.move(move) == False:
			print(f"Illegal move!")
		else:
			game.printBoard()
			print("")

	# Game Ended
	print(f"Game ended, player {game.winner} won.")
	return

if __name__ == "__main__":
	game = Shiftago()

	minimax = Minimax(ratios=(1, 5), depth=2)
	human = Human()

	play(game, minimax, human)