"""Items related to testing the game class."""
import pickle

from source.game.piece import Piece
from source.game.game import Game
from source.game.player import Player
from source.game.board import Board
from source.game.parser import Parser
import os


class TestGame:
    """Tests for the Game class."""

    def test_move(self):
        """
        Focus on moving pieces using the movement methods that sequentially update the board state.
        Uses a bunch of stuff, including the Parser.
        """

        # Load the test level. 
        test_level_path = os.path.join('source', 'game', 'tests', 'resources', 'test_game_level')

        # Parse the test file into a string.
        board_file = open(test_level_path, 'r')
        board_string = board_file.read()
        board_file.close()

        # Create Game using the newly-created board_string.
        game = Game.new_game(board_string)

        # Make sure first and second player can alternate moves.
        resp = game.make_move([0,0], [2,2])
        assert resp.move_status is True
        resp = game.make_move([6,6], [4,4])
        assert resp.move_status is True        

        # Make sure that moves out of order are not allowed.
        resp = game.make_move([4,4], [6,6])
        assert resp.move_status is False
        
        # Make sure that moves that don't target a piece are not allowed.
        resp = game.make_move([0,0], [2,2])
        assert resp.move_status is False
        
        # Make sure that moves that illegally move a piece are not allowed.
        resp = game.make_move([2,2], [5,5])
        assert resp.move_status is False

        # Try another legal move.
        resp = game.make_move([2,2], [0,0])
        assert resp.move_status is True
        
    def test_restore(self):
        """
        Focus on making moves with storing and restoring game objects.
        """
        
        # Load the test level. 
        test_level_path = os.path.join('source', 'game', 'tests', 'resources', 'test_game_level')

        # Parse the test file into a string.
        board_file = open(test_level_path, 'r')
        board_string = board_file.read()
        board_file.close()

        # Create Game using the newly-created board_string.
        game = Game.new_game(board_string)

        # Restore the game.
        restored_game = Game.restore(game)

        # Make sure first and second player can alternate moves post-restore.
        resp = restored_game.make_move([0,0], [2,2])
        assert resp.move_status is True
        resp = restored_game.make_move([6,6], [4,4])
        assert resp.move_status is True
        
        # Restore the game.
        restored_game = Game.restore(game)
        
        # Make sure that the position of pieces are stored properly.
        resp = restored_game.make_move([2,2], [0,0])
        assert resp.move_status is True
        resp = restored_game.make_move([4,4], [6,6])
        assert resp.move_status is True

    def test_can_be_pickled(self):
        """
        Validate that the game can be pickled and unpickled successfully.
        """
        
        # Load the test level. 
        test_level_path = os.path.join('source', 'game', 'tests', 'resources', 'test_game_level')

        # Parse the test file into a string.
        board_file = open(test_level_path, 'r')
        board_string = board_file.read()
        board_file.close()
        
        # Create Game using the newly-created board_string.
        game = Game.new_game(board_string)

        pickled_data = pickle.dumps(game)
        restored_game = pickle.loads(pickled_data)

        assert restored_game.console.board.create_display_string() == game.console.board.create_display_string()
