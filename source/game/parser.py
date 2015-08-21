""" Contains the singleton GameParser object and its global methods. """

from .piece import Piece
from .logger import logger
from .player import Player


class Parser:
    """
    Contains a set of methods to help create a Board from
    an input file.
    Sample File:

    1 . .
    . . .
    . . 2

    or

    1..1
    2.X2
    3x.3

    TODO:
    * Have area after the gameboard to supply input parameters for the players.

    Ex:

    Level:
    1..1
    2.X2
    3x.3

    Players:
    1:role=Human
    2:role=CPU,ai=super_fun
    3:role=CPU,ai=kitty
    """

    @staticmethod
    def convert_char_to_player_id(char):
        """
        Method used to take an input character from a level
        and assign a player to it.
        One approach to a switch statement in python:
        http://www.pydanny.com/why-doesnt-python-have-switch-case.html

        :param char: Character to convert to player.
        :type char: char
        :return: The owning player.
        :rtype: int
        """
        return {
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            'x': 0,
            'X': 0,
        }.get(char, 0)

    @staticmethod
    def is_piece(char):
        """
        Method used to determine if a character is a piece.
        Currently, everything besides an empy space is
        considered a piece.

        :param char: Input character to be considered.
        :type char: char
        :return: If it is a piece.
        :rtype: bool
        """
        return {
            '.': False,
        }.get(char, True)

    @staticmethod
    def find_player(player, game_board):
        """
        Method that attempts to locate a player by index
        in the provided board.

        :param player: Potential player to find.
        :type player: int
        :param game_board: The current board.
        :type game_board: Board
        :return: The player if found, None otherwise.
        :rtype: Player
        """
        for x in game_board.players:
            if x.id == player:
                return x
        return None

    @staticmethod
    def populate_player_from_char(char, game_board):
        """
        Method to populate a player from a character.
        Looks to see if this player has already been seen
        and returns an existing player accordingly.

        :param char: Character to search from.
        :type char: char
        :param game_board: The current board.
        :type game_board: Board
        :return: Existing player if found, new player otherwise.
        :rtype: Player
        """
        player_id = Parser.convert_char_to_player_id(char)
        player = Parser.find_player(player_id, game_board)
        if (player is None):
            player = Player(player_id)
            game_board.add_player(player)
            logger.debug("Creating new player=%u", player.id)
        return player

    @staticmethod
    def parse_file(file, game_board):
        """
        Method used to parse in input file and
        populate a gameboard object with various game elements.

        :param file: Level file to parse.
        :type file: File
        :param game_board: Fully populated Board object.
        :type game_board: Board
        """
        file = open(file, "r")

        # Operate over each line of the passed file and look for Pieces.
        height = 0
        width = 0
        for line in file.readlines():
            width = 0
            for char in line.split():
                # When one is found, add to the Board and perhaps add a Player.
                if Parser.is_piece(char):
                    player = Parser.populate_player_from_char(char, game_board)
                    new_piece = Piece(player,
                                      width,
                                      height,
                                      char)
                    game_board.add_piece(new_piece)
                width += 1
            height += 1

        # TODO - This has a potential bug if a non-rectangular level is used.
        # Would have to calculate a max length and width, and use that.
        # Or just do things differently. Or fill all non-rectangular areas with Xs.
        game_board.width = width
        game_board.height = height

        logger.debug("Parsed level name=%s with width=%u height=%u pieces=%u players=%u",
                     file.name,
                     width,
                     height,
                     len(game_board.pieces),
                     len(game_board.players))
