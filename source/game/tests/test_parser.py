"""Items related to testing the parser class."""

from source.game.parser import Parser
from source.game.board import Board
from source.game.player import Player
from source.game.piece import Piece
from source.game.zone import Zone
import os



class TestParser:
    """Tests for the Parser class and methods."""
        
    def test_parse_file(self):
        """ 
        Test the parser by constructing a Board from a file.
        Validate that all expected Pieces and Players have been created. 
        """

        # Make input file directory location os-agnostic. 
        test_level_path = os.path.join('source', 'game', 'tests', 'resources', 'test_level_1')

        # Parse the test file into a Board object.
        sample_game_board = Board()
        Parser.parse_file(test_level_path, sample_game_board)

        # Validate that board is the correct size and all related objects are created.
        assert sample_game_board.width is 5
        assert sample_game_board.height is 5
        assert len(sample_game_board.pieces) is 5
        assert len(sample_game_board.players) is 4
        assert len(sample_game_board.zones) is 1

    def test_parse_string(self):
        """ 
        Test the parser by constructing a Board from a string.
        Validate that all expected Pieces and Players have been created. 
        """

        # Make input file directory location os-agnostic. 
        test_level_path = os.path.join('source', 'game', 'tests', 'resources', 'test_level_1')
                
        # Parse the test file into a Board object.
        sample_game_board = Board()
        board_file = open(test_level_path, 'r')
        board_string = board_file.read()
        board_file.close()
        Parser.parse_string(board_string, sample_game_board)

        # Validate that board is the correct size and all related objects are created.
        assert sample_game_board.width is 5
        assert sample_game_board.height is 5
        assert len(sample_game_board.pieces) is 5
        assert len(sample_game_board.players) is 4
        assert len(sample_game_board.zones) is 1

