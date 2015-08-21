"""This file contains the implementation for managing player data."""


class Player:
    """The class for player data."""
    number_of_players = 0

    def __init__(self, index):
        """
        Constructor for Player class.

        :param index: The numberic identity of the player.
        :type index: int

        TODO:
        * Need to differentiate between human and cpu players.
        * For CPU players, need to specify AI module.
        """
        Player.number_of_players += 1
        self.id = index
