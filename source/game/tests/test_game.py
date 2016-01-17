"""Items related to testing the console class."""
from source.game.piece import Piece
from source.game.game import Game
from source.game.player import Player
from source.game.board import Board


class TestGame:
    """Tests for the Game class."""

    def test_move(self):
        """
        Focus on moving pieces using the movement methods that sequentially update the board state.
        """
        
        # Create a board.
        board = Board()
        
        # Create players and pieces for the game's board.            
        first_cached_player = Player(0)
        board.add_player(first_cached_player)
        board.add_piece(Piece(first_cached_player, 0, 0, 0))
        
        second_cached_player = Player(1)
        board.add_player(second_cached_player)
        board.add_piece(Piece(second_cached_player, 6, 6, 1))
            
        # Create game.
        game = Game.new_game(board)
        
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
        
        # Create a board.
        board = Board()
        
        # Create players and pieces for the game's board.            
        first_cached_player = Player(0)
        board.add_player(first_cached_player)
        board.add_piece(Piece(first_cached_player, 0, 0, 0))
        
        second_cached_player = Player(1)
        board.add_player(second_cached_player)
        board.add_piece(Piece(second_cached_player, 6, 6, 1))
        
        # Create game.
        game = Game.new_game(board)
                
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