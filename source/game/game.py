""" Defines object that provides interfaces to those that drive the game. """
from source.game.console import Console
from source.game.parser import Parser
from source.game.board import Board


class Game:
    
    """
    Game describes the top-level object that controls a game of colonies.
    This is the outward-facing object that other subsystems will interact with.
    """
    
    def __init__(self, console):
        """
        Constructor for a game object. Contains console object that contains game state.
        Not to be called implicitly by outside callers. Call new_game() instead.
        :param console: Passed console that contains game state.
        :type Console
        """
        self.console = console
        self.status = True
        self.board = self.console.board.create_display_string()
        
    @staticmethod
    def new_game(string_board):
        """
        Create and return a new game with all the required components.
        :param board: Passed board in string form that contains players and pieces.
        :type string
        :return: A new game.
        :rtype: Game
        """        
        board = Board()
        Parser.parse_board(string_board, board)
        console = Console(board)
        return Game(console)  

    def obtain_state(self):
        """
        Obtain a snapshot of the game state.
        :return: Current state object.
        :rtype: State
        """        
        return State(self.console.board.create_display_string())
    
    @staticmethod
    def restore(game):
        """
        Create a return a game from a blob of data.
        :param game: Byte stream of the previous game.
        :type opaque data
        :return: A familiar game.
        :rtype: Game
        """
        return Game(game.console)

    def make_move(self, piece_coord, move_coord):
        """
        Make a move given a coordinate for a piece and coordinate on where to move it.
        :param piece_coord: X and Y coordinates of the piece's location.
        :type piece_coord: list
        :param move_coord: X and Y coordinates where to move the piece.
        :type move_coord: list  
        :return: Response of the move.
        :rtype: Response
        """
        status = self.console.passive_move_interface(piece_coord, move_coord)
        resp  = Response(status, "No message... Yet.", self.obtain_state())
        self.status = status
        self.board = self.obtain_state().state_string
        return resp

class State:

    def __init__(self, state):
        """
        Constructor for a object that conveys board state. Currently in the form of a string.
        Not to be created implicitly by outside callers. Use obtain_state in the context of the Game object.
        :param state: State of the game in string form.
        :type state: string
        """
        self.state_string = state

class Response:
    
    def __init__(self, status, message, state):
        """
        Constructor for a response. Not be to called implicitly.
        Obtained from make_move() method in the Game object.
        :param status: True if the related operation is successful, false otherwise.
        :type status: boolean
        :param message: Any returned string from the related operation.
        :type message: string
        :param state: State of the game.
        :type state: State        
        """
        self.move_status = status
        self.message = message
        self.state = state    
    
        
        
    