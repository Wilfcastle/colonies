""" Defines GameBoard object and methods. """


class Board:
    """Board describes the area where a game is played. """

    number_of_boards = 0

    def __init__(self, width=0, height=0):
        """
        Constructor for a Board.
        :param width: The width of the board.
        :type width: int
        :param height: The height of the board.
        :type height: int
        """
        self.width = width
        self.height = height
        self.number_of_boards += 1
        self.pieces = []
        self.players = []

    def add_piece(self, piece):
        """
        Method that adds a piece to the pieces list of the board.
        :param piece: The piece to add.
        :type piece: Piece
        """
        self.pieces.append(piece)

    def add_player(self, player):
        """
        Method that adds a player to the board.
        :param player: The player to add.
        :type player: Player
        """
        self.players.append(player)

    def display_text_board(self):
        """Displays the game board in text format."""

        display_string = ""

        # Operate over a copy of the list of pieces.
        # Could sort by y & x to save a lot of time.
        temp_pieces = self.pieces
        for y in range(self.height):
            for x in range(self.width):

                # Attempt to find a piece for the new slot.
                piece_found = False
                for piece in temp_pieces:
                    if piece.width == x and piece.height == y:
                        display_string += str(piece.type)
                        temp_pieces.remove(piece)
                        piece_found = True

                # If a piece hasn't been found, place an empty space.
                if piece_found is False:
                    display_string += '.'
                display_string += ' '
            display_string += '\n'
        print(display_string)
