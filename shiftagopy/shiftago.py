import numpy as np

class Shiftago():
    def __init__(self, winning_length = 5, size = 7):
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int8)
        self.winning_length = winning_length

        self.turn = 1
        self.winner = None
        self.game_end = False

    def move(self, move):
        if self.game_end == True:
            return
        
        # Invalid move
        if move < 0 and move > (self.size * self.size - 1):
            return False
        
        self.mutate_board(move)

        # Switch turns
        self.turn = 1 if self.turn == 2 else 2

        # Check for end states
        result = self.check_end()
        if result != 0:
            self.winner = result
            self.game_end = True
        
        return True
    
    def mutate_board(self, move):
        side, number = move // self.size, move % self.size

        # From the top
        if side == 0:
            if self.check_insertion(self.board[:, number]):
                raise Exception("Cannot insert into filled column.")
            else:
                self.shift_col(number, direction=1)
                # Insert marble at edge
                self.board[0, number] = self.turn
        # From the right side
        elif side == 1:
            if self.check_insertion(self.board[number, :]):
                raise Exception("Cannot insert into filled row.")
            else:
                self.shift_row(number, direction=-1)
                # Insert marble at edge
                self.board[number, self.size - 1] = self.turn
        # From the bottom
        elif side == 2:
            if self.check_insertion(self.board[:, number]):
                raise Exception("Cannot insert into filled column.")
            else:
                self.shift_col(self.size - 1 - number, direction=-1)
                # Insert marble at edge
                self.board[self.size - 1, self.size - 1 - number] = self.turn
        # From the left side
        elif side == 3:
            if self.check_insertion(self.board[number, :]):
                raise Exception("Cannot insert into filled row.")
            else:
                self.shift_row(self.size - 1 - number, direction=1)
                # Insert marble at edge
                self.board[self.size - 1 - number, 0] = self.turn

        return
    
    # Check if row still has space to insert marble
    def check_insertion(self, row):
        return sum(row == 0) == 0
    
    def shift_row(self, row_n, direction):
        # No check for fullness of row necessary
        collected = []
        empty_idx = -1

        if direction == 1:
            for idx in range(0, self.size):
                if self.board[row_n, idx] == 0:
                    empty_idx = idx + 1
                    break
                else:
                    collected += [self.board[row_n, idx]]

            # Add the collected marbles in, shifted one to the right
            self.board[row_n] = np.concatenate((
                [0], 
                collected,
                self.board[row_n, empty_idx:]
            ))
        
        if direction == -1:
            for idx in reversed(range(0, self.size)):
                print(idx, self.board[row_n, idx])
                if self.board[row_n, idx] == 0:
                    empty_idx = idx
                    break
                else:
                    collected += [self.board[row_n, idx]]

            # Add the collected marbles in, shifted one to the right
            print(collected, empty_idx)
            self.board[row_n] = np.concatenate((
                self.board[row_n, :empty_idx],
                list(reversed(collected)),
                [0]
            ))
        
        return
    
    def shift_col(self, col, direction):
        # Rotate board then shift rows
        self.board = np.rot90(self.board)
        self.shift_row(self.size - 1 - col, direction)
        self.board = np.rot90(self.board , 3)
        return
    
    def check_end(self):
        for i in range(self.size):
            # vertical
            v = self.check_direction(0, i, 1, 0)
            if v != 0:
                return v
            
            # horizontal
            h = self.check_direction(i, 0, 0, 1)
            if h != 0:
                return h

        diagonals_top = [(0, c) for c in range(self.size - self.winning_length + 2)]
        
        for r, c in diagonals_top:
            # diagonal \
            d = self.check_direction(r, c, 1, 1)
            if d != 0:
                return d
            # diagonals /
            d = self.check_direction(r, self.size - 1 - c, 1, -1)
            if d != 0:
                return d
        
        # Exclude top left square
        diagonals_left = [(r + 1, 0) for r in range(self.size - self.winning_length + 1)]
        for r, c in diagonals_left:
            # diagonal \
            d = self.check_direction(r, c, 1, 1)
            if d != 0:
                return d
            # diagonals /
            d = self.check_direction(r, self.size - 1 - c, 1, -1)
            if d != 0:
                return d
            
        return 0

    def check_direction(self, row, col, rd, cd):
        count = 0
        player = 1
        other_player = 2

        for i in range(0, self.size):
            r = row + i * rd
            c = col + i * cd
            if r >= 0 and c >= 0 and r < self.size and c < self.size:
                if self.board[r, c] == player:
                    count += 1
                    if count >= self.winning_length:
                        return player
                elif self.board[r, c] == other_player:
                    count = 1
                    player, other_player = other_player, player
                else:
                    count = 0

        return 0