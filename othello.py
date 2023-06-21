# Author: Joel Strong
# GitHub username: jdstrongpdx
# Date: 5/18/23
# Description: Creates the logic and structures to play the board game Othello.  See the docstrings for specific
#               class and method descriptions for how the game works.
# Assignment: Portfolio Project

"""NOTE: THE DESIGN OF THIS PROGRAM COULD BE GREATLY OPTIMIZED, BUT WAS DESIGNED TO PRODUCE CERTAIN OUTPUTS FROM
CERTAIN METHODS FOR TESTING/GRADING PURPOSES FOR CLASS"""

def main():
    """Main function for running game"""
    game = Othello()
    game.auto()


class Player:
    """Represents a player in the board game.  Player objects will be stored in Othello class variable
        self._game['players'] as id: Player object.  Player objects are used by the Othello class to display
        the name and color of the winner of the game.
    :param str name: the name of the player
    :param str color: the color of the player (either 'white' or 'black')
    """
    def __init__(self, name: str, color: str):
        self._name = name
        self._color = color

    def get_player(self):
        """Return the name and color of the player
        :return name and color of self"""
        return self._name, self._color


class Othello:
    """Represents the board game Othello.  Contains two inner classes: Tile - which represents a single Tile
        on the board, and Piece - which represents Pieces played onto Tiles.  Othello class contains the data and
        methods to run the game, Tile objects hold the state of the current board, Piece objects hold the state of
        each piece played on Tile objects.  Player objects are used by the Othello class to display
        the name and color of the winner of the game.
    :ivar dict game: stores the data needed to run the game
    :ivar list board: stores the nested list of what symbol exists at each [x, y] coordinate in the game
    """

    def __init__(self):
        self._game = {'turn': 0, "piece_counter": 0, "player_counter": 0, "over": 0, "auto": 0,
                      "no_moves": 0, "tiles": {}, "pieces": {}, "players": []}
        self._board = []            # board to store nested list of current board
        self.initialize_game()      # run the initializer to create game

    class Piece:
        """Represents a playing piece that is played on Tile objects.  There are 62 Piece objects that can
            be possibly played.  Once set on a Tile, a piece cannot be moved, and once all Pieces have been
            played, the game is over.  Piece objects are stored in self._game["pieces"] as piece_id: color pairs.
            Piece objects are 'played' onto Tile objects to track the current state of the board.  Piece is an inner
            class of Othello.
        :param int number: the id number of the piece
        :param int color: the color of the piece (0 = black, 1 = white)
        :param Othello outer: the self object from the outer class (Othello) for calling methods from the outer class
        """
        def __init__(self, number: int, color: int, outer):
            self._piece_id = number
            self._color = color
            self._outer = outer

        def get_color(self) -> int:
            """Return the color of self
            :return color of self"""
            return self._color

        def change_color(self) -> None:
            """Flip the color of the Piece object
            :return None"""
            self._color = int(not self._color)
            return

    class Tile:
        """Represents an individual tile on a playing board with an x, y coordinate pair.  Tile objects either store
            an integer that represents the value to print or a Piece object (that will be either white or black).
            Integers were chosen as values over symbols for a more extensible design.  Adding/changing symbols can be
            done in the symbol lists in the print_board AND board_to_list methods.  Tile objects are stored in
            self._game["tiles"] as xy: item pairs.  Tile is an inner class of Othello.
        :param int x: the x coordinate of the tile
        :param int y: the y coordinate of the tile
        :param item: the value to be stored at the x,y coordinate pair
        :param Othello outer: the self object from the outer class (Othello) for calling methods from the outer class
        """
        def __init__(self, x: int, y: int, item: int, outer):
            self._coord = x * 10 + y
            self._item = item
            self._outer = outer

        def get_tile(self) -> int:
            """Return the item value of self or the color of the Piece object played on the Tile
            :return integer value of the current state of the Tile - 0 = black, 1 = white, 2 = border, 3 = blank"""
            if type(self._item) == int:
                return self._item
            elif type(self._item) == Othello.Piece:
                piece = self._item
                return piece.get_color()

        def flip_piece(self) -> None:
            """Flips the color of a Piece object on a Tile
            :return None"""
            if type(self._item) == int:
                return
            elif type(self._item) == Othello.Piece:
                self._item.change_color()
                return

        def set_piece(self, color) -> None:
            """Pulls a Piece from the stock, sets the color and places the Piece object on a Tile
            :param color: the color of the piece to place
            :return None"""
            piece = self._outer.get_piece()
            if color == "white":            # pieces are initialized as black, so flip if white piece is played
                piece.change_color()
            self._item = piece
            return

    def initialize_game(self) -> None:
        """Initializes the Tiles, Pieces, starting positions, and self._board before the start of each game.
            --- Create Tile objects for each x, y coordinate in the game, set initial value, and store objects.
            --- Create 62 Piece objects for the game, set initial value to black, and store objects.
            --- Place the four starting pieces on the board
            --- Generate the current board state out of Tile/Piece objects and store as a nested list matrix in
                 self._board.
            :return: None
        """
        # init Tiles
        for x in range(10):
            for y in range(10):
                name = x * 10 + y
                if x == 0 or x == 9 or y == 0 or y == 9:
                    item = 3   # will print " * "
                else:
                    item = 2   # will print " . "
                self._game["tiles"][name] = Othello.Tile(x, y, item, self)

        # init Pieces
        for item in range(64):
            self._game["pieces"][item] = Othello.Piece(item, 0, self)

        # init starting positions  NOTE: COORDINATES ARE BASED ON X,Y STARTING FROM TOP LEFT CORNER
        init_dict = {44: "white", 45: "black", 55: "white", 54: "black"}
        for item in init_dict:
            tile = self._game["tiles"][item]
            color = init_dict[item]
            tile.set_piece(color)

        # init the board to the starting values for the game
        self._board = self.board_to_list()
        return

    def get_piece(self):
        """Return the current piece counter and increment the counter:
        :return: the next available piece object or None if out of pieces"""
        counter = self._game["piece_counter"]
        if counter >= 63:
            return None
        self._game["piece_counter"] += 1
        return self._game["pieces"][counter]

    def print_board(self) -> None:                              # REQUIRED
        """Using the current state of the Tile and Piece objects, print board to the console
        :return: None"""
        symbol = [" X ", " O ", " . ", " * "]
        for item in self._game["tiles"]:
            tile = self._game["tiles"][item].get_tile()
            print(symbol[tile], end="")
            if item % 10 == 9:
                print()
        return

    def create_player(self, name: str, color: str) -> None:
        """Create a player with a name and piece color using error checking.
        :param str name: the name of the player
        :param str color: the color of the players pieces
        :return: None
        """
        if self._game["player_counter"] == 2:                                   # if more than 2 players are entered
            print('A maximum of two players are allowed')
            return
        elif not name:                                                          # if no name is entered
            print('A valid name must be entered.')
            return
        elif (color.lower() != "black") and (color.lower() != "white"):         # if the colors are not black or white
            print('The color must be "white" or "black".  Please try again')
            return
        elif self._game["player_counter"] == 1:                                 # if the same color is entered twice
            first_name, first_color = self._game["players"][0].get_player()
            if first_color == color:
                print("Players must select different colors.")
                return
        self._game["players"].append(Player(name, color))                       # create the Player
        self._game["player_counter"] += 1
        return

    def return_winner_count(self) -> tuple:
        """Return the current number of black and white Pieces played on the board
        :return black_count, white_count"""
        black_count, white_count = 0, 0
        for item in self._game["tiles"]:
            tile = self._game["tiles"][item].get_tile()
            if tile == 1:
                white_count += 1
            elif tile == 0:
                black_count += 1
        return black_count, white_count

    def return_winner(self) -> str:                            # REQUIRED
        """Use helper method (return_winner_count) to count the number of each color on the board
            and return the winner of the game at any point
        :return str: a string value for the winner of the game or None if there is an error
        """
        black_count, white_count = self.return_winner_count()
        players = {}
        for player in self._game["players"]:
            player_name, player_color = player.get_player()
            players[player_color] = player_name
        if black_count > white_count:
            return 'Winner is black player: ' + str(players["black"])
        elif black_count == white_count:
            return "It's a tie"
        else:
            return 'Winner is white player: ' + str(players["white"])

    def return_available_positions(self, color: str) -> list:        # REQUIRED
        """Return a list of possible positions for the player with the given color to move on the current board.
            --- Will first find all Pieces on the board of the parameter color.
            --- For each Piece on the board, it will search in each direction for valid moves - left, left-up, up,
                    right-up, right, right-down, down, left-down  (using helper function positions_helper)
            --- Appends the possible moves to a list and returns a list of Tuple coordinates for valid moves
        :param str color: the color of the current player
        :return list moves: a list of all valid moves for the parameter color
        """
        move_list = []
        if color.lower() == "black":
            color = 0
        else:
            color = 1
        # get a list of colored pieces on the board to iterate through
        pieces = [item for item in self._game["tiles"] if self._game["tiles"][item].get_tile() == color]
        for coord in pieces:
            x = coord % 100 // 10                     # break coordinate into constituents
            y = coord % 10
            directions = [[1, 0], [1, 1], [0, 1], [-1, 1], [0, -1], [-1, -1], [-1, 0], [1, -1]]
            for direction in directions:        # try moves in each direction
                possible = self.positions_helper(x, y, direction, color)
                if possible:                    # if a move is valid,
                    if possible not in move_list:   # check if move is already in the list (no duplicates)
                        move_list.append([possible[0], possible[1]])
        if not move_list:
            return []
        else:
            move_list.sort()
            move_list = [tuple(coord) for coord in move_list]
        return move_list

    def positions_helper(self, x: int, y: int, direction: list, color: int):
        """Helper function that returns the first valid move of any directional sequence or None
            From any given coordinate, search a single direction for the following:
             --- if players own piece or a border piece is first, no move for that direction
             --- if an opposing players piece (or multiple), check there is a blank tile to play on after
                    if not, no moves, if yes, return move position
        :param int x: the x coordinate of the current position
        :param int y: the y coordinate of the current position
        :param list direction: the x,y coordinates for the direction to try
        :param int color: the current player's color
        :return: the [x,y] coordinate of a valid move in the specified direction or None if no valid move.
        """
        find_color = not color                      # find pieces of the opposite color
        count = 1                                   # counts number of tiles moved
        x1, y1 = direction[0], direction[1]
        while 0 < x < 9 and 0 < y < 9:              # keep moves on the board
            x = x + x1
            y = y + y1
            find_coord = x * 10 + y                 # calculate next move
            tile = self._game["tiles"][find_coord].get_tile()
            if count == 1 and tile != find_color:   # if the first object is not a piece of opposing color - exit
                return
            elif count > 1 and tile == 2:           # if first empty space after n number of opposing colors - return
                return [x, y]
            elif tile == color or tile == 3:        # if a piece of own color or border - exit
                return
            count += 1

    def board_to_list(self) -> list:
        """Return a nested list of string objects corresponding the current state of the Tile and Piece objects
           --- used to generate the current state of self._board
        :return list output: a nested list matrix of the current state of all Tiles on the board
        """
        output = []
        nested = []
        symbol = ["X", "O", ".", "*"]
        for item in self._game["tiles"]:
            tile = self._game["tiles"][item].get_tile()
            nested.append(symbol[tile])
            if item % 10 == 9:
                output.append(nested)
                nested = []
        return output

    def make_move(self, color: str, piece_position: tuple) -> list:         # REQUIRED
        """WARNING - METHOD ASSUMES THAT MOVES ENTERED ERROR-CHECKED/VALID BEFORE METHOD
            --- From a given coordinate, use a helper method (flip_pieces) find the Piece objects that need to be
                    flipped in each direction from the newly played piece
            --- Flip all the Piece objects found by the helper method
            --- Generate the current state of the board and save to self._board
            --- Return a list of the new board positions.
            :param str color: the string value for the current players color (black or white)
            :param tuple piece_position: the (x, y) coordinate of the move position
            :return list self._board: the current state of the board
            """
        position = piece_position[0] * 10 + piece_position[1]
        tile = self._game["tiles"][position]
        if type(tile.get_tile()) == int:
            tile.set_piece(color)          # if empty tile, set new piece
        else:
            tile.flip_piece()              # else, flip piece on tile

        # flips all valid lines between the played piece and existing pieces
        directions = [[1, 0], [1, 1], [0, 1], [-1, 1], [0, -1], [-1, -1], [-1, 0], [1, -1]]
        for direction in directions:  # try moves in each direction
            flip_list = self.flip_piece(direction, piece_position, color)
            if flip_list:
                for piece in flip_list:
                    self._game["tiles"][piece].flip_piece()
        self._board = self.board_to_list()
        return self._board

    def flip_piece(self, direction: list, piece_position: tuple, color: str):
        """Helper function for make_move that will correctly flip all Piece objects in all directions between
            the existing Pieces on the board and the latest played Piece.
        :param list direction: the current x,y coordinates of the direction to try
        :param list piece_position: the current x, y coordinates of the current position
        :param int color: the integer value for the current players color (0=black, 1=white)
        :return flip_list: return a tuple of all Piece objects that need to be flipped for the given direction or None
        """
        if color == "black":
            find_color = 1
        else:
            find_color = 0
        x, y = piece_position[0], piece_position[1]
        x1, y1 = direction[0], direction[1]
        flip_list = []
        while 0 < x < 9 and 0 < y < 9:          # keep moves on the board
            x = x + x1
            y = y + y1
            find_coord = x * 10 + y             # calculate next move
            tile = self._game["tiles"][find_coord]
            if tile.get_tile() == (not find_color):
                return flip_list
            flip_list.append(find_coord)
        return

    def play_game(self, player_color: str, piece_position: tuple):  # REQUIRED
        """Ties the other methods of Othello together to 'play the game' one move at a time
            NOTE: DOES NOT ERROR CHECK THE OFFICIAL RULES OF THE GAME
            --- Get a current list of valid moves for the player color
            --- If there are no moves for both players or if there are no more Pieces to play, game is over
            --- Check that the parameter move is a valid move, and print/return message if invalid
            --- If valid, make the move, and update/return the current state of the board
        :param str player_color: a string value for the players color (white or black)
        :param tuple piece_position: the (x, y) coordinates of the position to be played
        :return: None if a move is valid, "Invalid move" is a move is invalid
        """
        moves = []
        if piece_position[0] > 9 or piece_position[1] > 9:
            print(f"Invalid move. Here are the valid moves: {moves}")
            return "Invalid move"
        coord = piece_position[0] * 10 + piece_position[1]
        tile = self._game['tiles'][coord]
        moves = self.return_available_positions(player_color)                         # get valid moves
        if not moves:                                                                 # if there are no valid moves
            if self._game["no_moves"] == 1:                                           # if both players have no moves
                self._game["over"] = 1
                black_count, white_count = self.return_winner_count()                 # get/print counts
                print(f"Game is ended white piece: {white_count} black piece: {black_count}")
                print(self.return_winner())                                           # call return_winner
                return
            else:
                self._game["no_moves"] += 1
        else:
            self._game["no_moves"] = 0                                                # reset the moves counter
        if piece_position not in moves or tile.get_tile() != 2:                       # if the move is not valid/empty
            print(f"Invalid move. Here are the valid moves: {moves}")
            return "Invalid move"
        else:
            self.make_move(player_color, piece_position)                              # make move

    def auto(self) -> None:
        """Uses existing methods to allow a game to be played between two players - ending the game when
        there are no more moves for either player or no more pieces to play."""
        self._game["auto"] = 1
        self._game["over"] = 0
        name = input("Please enter the first players name: ")
        self.create_player(name, "black")
        name = input("Please enter the second players name: ")
        self.create_player(name, "white")
        print("The first player will be black(X) and will go first.  "
              "The second player will be white(O) and will go second.\n"
              "Coordinates are based on zero indexed positions from the top left corner.")
        players = {}
        for player in self._game["players"]:
            player_name, player_color = player.get_player()
            players[player_color] = player_name
        while not self._game["over"]:                       # run game until the game is over
            if self._game["piece_counter"] == 62:  # if there are no more pieces to play
                self._game["over"] = 1
                black_count, white_count = self.return_winner_count()  # get/print counts
                print("There are no more pieces to play.")
                print(f"Game is ended white piece: {black_count} black piece: {white_count}")
                print(self.return_winner())  # call return_winner
                return
            self.print_board()
            print()
            if self._game["turn"] == 0:
                color = "black"
                print(f"It is {players['black']}'s turn. You are the black (X) player.")
            else:
                print(f"It is the {players['white']}'s turn. You are the white (O) player.")
                color = "white"
            # check if there are valid moves, for one or both players, and if the game has ended.
            moves = self.return_available_positions(color)
            if moves:
                self._game["no_moves"] = 0
                print_moves = (', '.join(map(str, moves)))
                print(f"Your valid moves are: {print_moves}")
                flag = 0
                # NOTE - game over conditions are part of play_game and will toggle over flag
                while not flag:
                    try:
                        user_input = input("Please enter a move or type exit to quit: ")
                        if user_input == "exit":
                            print("Thank you for playing!")
                            return
                        user_input = user_input.split(",")
                        x = int(user_input[0])
                        y = int(user_input[1])
                        user_input = (x, y)
                        if user_input not in moves:
                            print("Invalid move")
                            raise TypeError
                        print(f"{players[color]}'s move is: {user_input}\n")
                        game_return = self.play_game(color, user_input)
                        if game_return == "Invalid move":
                            raise TypeError
                        self._game["turn"] = not self._game["turn"]
                        flag = 1
                    except (TypeError, IndexError, ValueError):
                        print("Invalid entry.  Please try again.")
            else:
                self._game["turn"] = not self._game["turn"]
                self._game["no_moves"] += 1
                if self._game["no_moves"] == 2:
                    print("There are no moves")
                    self.return_winner()
                    break


if __name__ == "__main__":
    main()
