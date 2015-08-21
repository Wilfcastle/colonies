"""Tests for the board class."""
import pytest
from game.board import Board


class TestBoard:
    """The Board class test suite."""
    @pytest.fixture
    def board(self):
        """
        Fixture to create a board object.
        :return: The board object.
        :rtype: Board
        """
        return Board()

    def test_add_piece_increases_the_size_of_pieces(self, board):
        """
        Test that adding a piece to the board increases the count of pieces.
        :param board: The board object
        :type board: Board
        """
        pre_length = len(board.pieces)
        board.add_piece(None)
        post_length = len(board.pieces)

        assert post_length == pre_length + 1
