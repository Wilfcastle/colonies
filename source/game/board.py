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
        self.zones = []

    def add_piece(self, piece):
        """
        Method that adds a piece to the pieces list of the board.

        :param piece: The piece to add.
        :type piece: Piece
        """
        self.pieces.append(piece)

    def add_zone(self, zone):
        """
        Method that adds a zone to the zone list of the board.
        :param zone: The zone to add.
        :type zone: Zone
        """
        self.zones.append(zone)

    def add_player(self, player):
        """
        Method that adds a player to the board.
        :param player: The player to add.
        :type player: Player
        """
        self.players.append(player)

    def does_player_have_pieces(self, player):
        """
        Method that checks if the provided player
        has any pieces on the board.
        :param player: The player to check.
        :type player: Player
        :return: If the passed player has any pieces.
        :rtype: bool
        """
        for piece in self.pieces:
            if piece.player is player:
                return True
        return False

    def create_display_string(self):
        """
        Creates a string from the board and returns it.
        :return: game-state in string form.
        :rtype: string
        """
        display_string = ""
        # Operate over copies of element lists.
        # Could sort by y & x to save a lot of time.
        temp_pieces = list(self.pieces)
        temp_zones = list(self.zones)
        for y in range(self.height):
            for x in range(self.width):

                # Attempt to find a zone for the new slot.
                # Some zones may be 'transparent', so pieces may overlap.
                element_found = False
                for zone in temp_zones:
                    if zone.x == x and zone.y == y:
                        new_char = str(zone.type)
                        temp_zones.remove(zone)
                        element_found = True
                        break

                # Attempt to find a piece for the new slot.
                for piece in temp_pieces:
                    if piece.x == x and piece.y == y:
                        new_char = str(piece.type)
                        temp_pieces.remove(piece)
                        element_found = True
                        break

                # If an element hasn't been found, place an empty space.
                if element_found is False:
                    new_char = '.'

                display_string += new_char
                display_string += ' '
            display_string += '\n'
        return display_string

    def display_text_board(self):
        """Displays the game board in text format."""
        print(self.create_display_string())
