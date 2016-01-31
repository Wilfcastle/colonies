""" Contains the singleton Parser object and its global methods. """

from .piece import Piece
from .zone import Zone
from .logger import logger
from .player import HumPlayer
from .player import ComPlayer
from enum import IntEnum
from io import StringIO # Only compatible with Python3

class Parser:

    """

    Contains a set of methods to help create a Board from
    an input file.
    Sample File:
    Players:
    P=1:role=HumPlayer
    P=2:role=ComPlayer:ai=super_fun
    Board:
    1 . .
    . . .
    . . 2
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
        }.get(char, 0)

    class Role(IntEnum):

        """  Describe types of roles for a Player for parsing. """
        none = 0
        human = 1
        cpu = 2

    @staticmethod
    def get_role_from_string(string):
        """
        Take an input string and return a role.

        :param string: string to convert to a role.
        :type string: string
        :return: The resulting Role.
        :rtype: Role
        """
        if string == "human":
            return Parser.Role.human
        elif string == "cpu":
            return Parser.Role.cpu
        else:
            return Parser.Role.none

    @staticmethod
    def is_piece(char):
        """
        Method used to determine if a character is a piece.

        :param char: Input character to be considered.
        :type char: char
        :return: If it is a piece.
        :rtype: bool
        """
        return {
            '1': True,
            '2': True,
            '3': True,
            '4': True,
            '5': True,
            '6': True,
            '7': True,
            '8': True,
        }.get(char, False)

    @staticmethod
    def is_zone(char):
        """
        Method used to determine if a character is a zone.

        :param char: Input character to be considered.
        :type char: char
        :return: If it is a zone.
        :rtype: bool
        """
        return {
            'X': True,
        }.get(char, False)

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
        if player is None and player_id is not 0:
            player = HumPlayer(player_id)
            game_board.add_player(player)
            logger.debug("Creating new undefined human player=%u", player.id)
        return player

    @staticmethod
    def parse_players_from_file(file, game_board):
        """
        Method used to parse an input file,
        populating all provided players with roles and
        ai script names where needed.

        :param file: Level file to parse.
        :type file: File
        :param game_board: Provided Board object.
        :type game_board: Board
        """
        logger.debug("Parsing Players:")

        # If this file doesn't have the Players: format,
        # then just reset it and parse the board itself.
        line = file.readline()
        if "Players:" not in line:
            file.seek(0)
            logger.debug("Players: not found. Parsing board normally.")
            return

        logger.debug("Found Players:")

        # Parse each Player line from the Players: section,
        # continuing until we find the end (Board:).
        while line:
            line = file.readline()
            line = line.strip()

            if "Board:" not in line:
                logger.debug("Done parsing Players:")
                return

            # Parse a new player.
            player_id = 0
            role = "NULL"
            ai = "NULL"
            types = line.split(':')
            for type in types:
                value = type.split('=')
                if value[0] is 'P':
                    player_id = Parser.convert_char_to_player_id(value[1])
                elif value[0] == "role":
                    role = Parser.get_role_from_string(value[1])
                elif value[0] == 'ai':
                    ai = value[1]

            # If a valid player has been detected, then add it.
            if player_id is not 0 and role is not Parser.Role.none:
                if role is Parser.Role.cpu:
                    new_player = ComPlayer(player_id, ai)
                    game_board.add_player(new_player)
                else:
                    new_player = HumPlayer(player_id)
                    game_board.add_player(new_player)

                logger.debug("Adding Player=%u, a %u type of Player with ai of %s.",
                             player_id,
                             role,
                             ai)
            else:
                logger.error("Invalid Player %u, role=%u ai=%s.",
                             player_id,
                             role,
                             ai)

    @staticmethod
    def parse_players(string, game_board):
        """
        Method to parse players from a string and assign to board.
        May or may not be needed. 
        :param string: String to parse.
        :type string: string
        :param game_board: Semi-populated Board object.
        :type game_board: Board
        """        
        return
        
    @staticmethod
    def parse_board(string, game_board):
        """
        Method to parse an input string and assign to a board.
        May or may not be needed. 
        :param string: String to parse.
        :type string: string
        :param game_board: Semi-populated Board object in, fully populated out.
        :type game_board: Board
        """
        logger.debug("Parsing Board:")
        height = 0
        width = 0
        string_board_io = StringIO(string)
        for line in string_board_io.readlines():
            width = 0
            for char in line.split():
                # When one is found, add to the Board and perhaps add a
                # Player.
                if Parser.is_piece(char):
                    player = Parser.populate_player_from_char(char, game_board)
                    new_piece = Piece(player,
                                      width,
                                      height,
                                      char)
                    game_board.add_piece(new_piece)
                elif Parser.is_zone(char):
                    new_zone = Zone(width,
                                    height,
                                    char)
                    game_board.add_zone(new_zone)

                width += 1
            height += 1

        # TODO - This has a potential bug if a non-rectangular level is used.
        # Would have to calculate a max length and width, and use that.
        # Or just do things differently. Or fill all non-rectangular areas with
        # Xs.
        game_board.width = width
        game_board.height = height

        logger.debug("Parsed board with width=%u height=%u pieces=%u players=%u",
                     width,
                     height,
                     len(game_board.pieces),
                     len(game_board.players))

    @staticmethod
    def parse_file(file, game_board):
        """
        Method used to parse in input file and
        populate a Board object with various game elements
        and players.
        :param file: Level file to parse.
        :type file: File
        :param game_board: Fully populated Board object.
        :type game_board: Board
        """
        file = open(file, 'r')
        Parser.parse_players_from_file(file, game_board)
        Parser.parse_board(file.read(), game_board)
        file.close()

    @staticmethod
    def parse_string(string_board, game_board):
        """
        Method used to parse in input string and
        populate a Board object with various game elements
        and players.
        :param string_board: String to parse.
        :type string_board: string
        :param game_board: Fully populated Board object.
        :type game_board: Board
        """
        # Only call the parse board method for now.
        # The details with player management will be worked out later.
        Parser.parse_board(string_board, game_board)