""" Plays the game of Colonies """
from itertools import cycle
from source.game.logger import logger
from sys import exit


class Console:

    def __init__(self, board):
        """
        Constructor for a console. 
        When initialized, the provided board must have at least one player.
        :param board: Provided game board object.
        :type board: Board
        """
        self.board = board
        self.active_player = self.board.players[0]


    def evaluate_board(self):
        """ Handles any updates on board state. Exits if there is a winner. """
        if self.is_winner() is True:
            logger.error("Player=%u has won!.", self.active_player.id)
            exit()

    def get_next_player(self):
        """ Switches to the next available player with pieces."""
        if self.active_player is None:
            self.active_player = self.board.players[0]
        else:
            players_cycle = cycle(self.board.players)

            # Cycle to the current player.
            for temp_player in players_cycle:
                if temp_player is self.active_player:
                    break

            # Cycle to the next available player with pieces.
            for temp_player in players_cycle:
                if (self.board.does_player_have_pieces(temp_player) is False):
                    continue
                self.active_player = temp_player
                break

        logger.debug("Starting turn for player=%u.", self.active_player.id)

    def take_turn(self):
        """
        Takes the current player's turn.
        :return: If the turn is successful.
        :rtype: bool
        """
        # Obtain the move from the current player.
        piece_coord, move_coord = self.active_player.make_move()
        if len(piece_coord) is not 2:
            logger.error("Invalid piece selection for player=%u. Need two coordinates not %u.",
                         self.active_player.id, len(piece_coord))
            return False
        
        return self.make_move(piece_coord, move_coord);
    
    def passive_move_interface(self, piece_coord, move_coord):
        """
        Treating the core as passive, make the move from the passed coordinates
        and progress the active player.
        :param piece_coord: X and Y coordinates of the piece's location.
        :type piece_coord: list
        :param move_coord: X and Y coordinates where to move the piece.
        :type move_coord: list   
        :return: If the turn is successful.
        :rtype: bool
        """
        if self.make_move(piece_coord, move_coord) is True:
            self.get_next_player()
            return True
        return False
        
    def make_move(self, piece_coord, move_coord):
        """
        Perform a move of a single piece.
        :param piece_coord: X and Y coordinates of the piece's location.
        :type piece_coord: list
        :param move_coord: X and Y coordinates where to move the piece.
        :type move_coord: list   
        :return: If the turn is successful.
        :rtype: bool
        """        
        x = piece_coord[0]
        y = piece_coord[1]
        # Check to make sure the chosen piece exists.
        piece_found = False
        for piece in self.board.pieces:
            if piece.x is x and piece.y is y:
                piece_found = True
                break

        if piece_found is False:
            logger.error("Could not find piece for player=%u at (%u,%u).",
                         self.active_player.id, x, y)
            return False

        if piece.player != self.active_player:
            logger.error("Piece owned by player=%u not player=%u at (%u,%u).",
                         piece.player.id, self.active_player.id, x, y)
            return False

        # Handle the suggested move.
        if len(move_coord) is not 2:
            logger.error("Invalid move selection for player=%u. Need two coordinates not %u.",
                         self.active_player.id, len(move_coord))
            return False
        x = move_coord[0]
        y = move_coord[1]

        # Check for piece collision.
        if self.does_cause_collision(x, y):
            logger.error("Invalid move selection for player=%u. Element exists at (%u,%u).",
                         self.active_player.id, x, y)
            return False

        # When move is made, attempt it.
        if piece.is_jump_distance(x, y):
            piece.jump(x, y)
        elif piece.is_clone_distance(x, y):
            new_piece = piece.clone(x, y)
            self.board.pieces.append(new_piece)
            piece = new_piece
        else:
            logger.error("Piece owned by player=%u not in range of jump or clone at (%u,%u).",
                         piece.player.id, x, y)
            return False

        self.check_for_capture(piece)
        return True

    def play(self):
        """ Play the game of colonies. Perform moves from different players until the game is over. """
        while (1):
            self.board.display_text_board()
            self.get_next_player()
            while self.take_turn() is not True:
                pass
            self.evaluate_board()

    def is_winner(self):
        """
        Iterate over all pieces and check to see if they all belong
        to the active player. If not, then there is no winner.
        :return: If there is a winner.
        :rtype: bool
        """
        for piece in self.board.pieces:
            if piece.player is not self.active_player:
                return False
        return True

    def check_for_capture(self, current_piece):
        """
        Evaluate the last action and check to see if any pieces can be captured.
        :param current_piece: The piece that has been acted on.
        :type current_piece: Piece
        """
        for piece in self.board.pieces:
            if piece.is_adjacent_to(
                    current_piece) and current_piece.player is not piece.player:
                piece.capture(current_piece.player)

    def does_cause_collision(self, x, y):
        """
        Determine if the new coordinates cause a collision.
        :param x: X-coordinate
        :type x: Int
        :param x: Y-coordinate
        :type x: Int
        :return: If this would cause collision.
        :rtype: Bool
        """
        # Check for pieces.
        for match_piece in self.board.pieces:
            if match_piece.x is x and match_piece.y is y:
                return True

        # Check for zones with collision.
        for match_zone in self.board.zones:
            if match_zone.x is x and match_zone.y is y and match_zone.collision:
                return True

        return False
