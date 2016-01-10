"""Items related to testing the console class."""
from source.game.board import Board
from source.game.piece import Piece
from source.game.console import Console
from source.game.player import Player



class TestConsole:
    """Tests for the Console class."""

    def test_passive_move_pieces(self):
        """
        Focus on moving pieces using the movement methods that sequentially update the board state.
        No capturing now.
        """
        
        # Create players and pieces for board..        
        board = Board()
        first_cached_player = Player(0)
        board.add_player(first_cached_player)
        board.add_piece(Piece(first_cached_player, 0, 0, 0))
        
        second_cached_player = Player(1)
        board.add_player(second_cached_player)
        board.add_piece(Piece(second_cached_player, 6, 6, 1))    
        
        # Create console with board. 
        console = Console(board)
        
        # Make sure first and second player can alternate moves.
        assert console.active_player.id is first_cached_player.id
        assert console.passive_move_interface([0,0], [2,2]) is True
        assert console.active_player.id is second_cached_player.id 
        assert console.passive_move_interface([6,6], [4,4]) is True
        assert console.passive_move_interface([2,2], [0,0]) is True
        assert console.passive_move_interface([4,4], [6,6]) is True
        
        # Make sure first player cannot control second player's pieces.
        assert console.active_player.id is first_cached_player.id
        assert console.passive_move_interface([6,6], [4,4]) is False
        assert console.active_player.id is first_cached_player.id
        assert console.passive_move_interface([0,0], [2,2]) is True
        assert console.active_player.id is second_cached_player.id
        
        # Make sure first player cannot move pieces onto second player's pieces.
        # Make sure false is passed back correctly.
        assert console.passive_move_interface([6,6], [4,4]) is True
        assert console.passive_move_interface([2,2], [4,4]) is False
        assert console.active_player.id is first_cached_player.id
        assert console.passive_move_interface([2,2], [0,0]) is True
