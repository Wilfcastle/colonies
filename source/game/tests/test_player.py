"""Tests for the Player class."""
import pytest
from game.player import Player


class TestPlayer:
    """The Player class test suite."""
    def test_creating_a_player_increases_the_player_count(self):
        """
        Checks that creating a player increases the player count with each player.
        """
        assert Player.number_of_players == 0
        player1 = Player()
        assert Player.number_of_players == 1
        player2 = Player()
        assert Player.number_of_players == 2
