""" Contains the singleton GameParser object and its global methods. """

from game.piece import Piece
from game.logger import logger


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
    """

    @staticmethod
    def convert_char_to_player(char):
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
    def parse_file(file, game_board):
        """
        Method used to parse in input file and
        populate a gameboard object with various game elements.
        TODO: Needs to populate a number of player objects.

        :param file: Level file to parse.
        :type file: File
        :param game_board: Fully populated Board object.
        :type game_board: Board
        """
        file = open(file, "r")

        # Operate over each line of the passed file and look for GamePieces.
        height = 0
        width = 0
        for line in file.readlines():
            width = 0
            for char in line.split():
                # When one is found, add to the Board.
                if Parser.is_piece(char):
                    new_piece = Piece(Parser.convert_char_to_player(char),
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

        logger.debug("Parsed level name=%s with width=%u height=%u", file, width, height)
