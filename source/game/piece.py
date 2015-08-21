""" Contains GamePiece object and methods """


class Piece:
    """ A Piece defines a generic unit that is involved in the game. """

    def __init__(self, player, width, height, piece_type):
        """
        Constructor for Piece class.

        :param player: The player which controls this piece. 0 is no player.
        :type player: int
        :param width: The X coordinate of the piece.
        :type width: int
        :param height: The Y coordinate of the piece.
        :type height: int
        :param piece_type: What type of piece it is.
        :type piece_type: int
        """
        self.player = player
        self.width = width
        self.height = height
        self.type = piece_type
        self.capture_count = 0
        self.move_count = 0

    def capture(self, player):
        """
        Used for passed Player to gain control of Piece

        :param player: The player to gain control of this Piece.
        :type player: Player
        """
        self.player = player
        self.capture_count = self.capture_count + 1

    def move(self, x, y):
        """
        Relocates the passed piece on the gameboard.

        :param x: The units of width to move this piece.
        :type x: int
        :param y: The units of height to move this piece.
        :type y: int
        """
        self.width = self.width + x
        self.height = self.width + y
        self.move_count = self.move_count + 1
