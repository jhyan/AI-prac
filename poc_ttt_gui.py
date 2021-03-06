"""
poc_ttt_gui.pu
Tic Tac Toe GUI code.
@Author  Rice  University. Revised by Jiahan Yan and Boyu Liu
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import poc_ttt_provided as provided

GUI_WIDTH = 400
GUI_HEIGHT = GUI_WIDTH
BAR_WIDTH = 5


class TicTacGUI:
    """
    GUI for Tic Tac Toe game.
    """

    def __init__(self, size, aiplayer, aifunction, ntrials, reverse=False):
        # Game board
        self._size = size
        self._bar_spacing = GUI_WIDTH // (self._size * self._size)
        self._turn = provided.PLAYERX
        self._reverse = reverse

        # AI setup
        self._humanplayer = provided.switch_player(aiplayer)
        self._aiplayer = aiplayer
        self._aifunction = aifunction
        self._parameter = ntrials

        # Set up data structures
        self.setup_frame()

        # Start new game
        self.newgame()

        # set valid region highlight
        self.boxrow_valid = None
        self.boxcol_valid = None

    def setup_frame(self):
        """
        Create GUI frame and add handlers.
        """
        self._frame = simplegui.create_frame("Ultimate Tic-Tac-Toe",
                                             GUI_WIDTH,
                                             GUI_HEIGHT)
        self._frame.set_canvas_background('White')

        # Set handlers
        self._frame.set_draw_handler(self.draw)
        self._frame.set_mouseclick_handler(self.click)
        self._frame.add_button("New Game", self.newgame)
        self._label = self._frame.add_label("")

    def start(self):
        """
        Start the GUI.
        """
        self._frame.start()

    def newgame(self):
        """
        Start new game.
        """
        self._board = provided.TTTBoard(self._size, self._reverse)
        self._inprogress = True
        self._wait = False
        self._turn = provided.PLAYERX
        self._label.set_text("")

    def drawx(self, canvas, pos):
        """
        Draw an X on the given canvas at the given position.
        """
        halfsize = .4 * self._bar_spacing
        canvas.draw_line((pos[0] - halfsize, pos[1] - halfsize),
                         (pos[0] + halfsize, pos[1] + halfsize),
                         BAR_WIDTH, 'Black')
        canvas.draw_line((pos[0] + halfsize, pos[1] - halfsize),
                         (pos[0] - halfsize, pos[1] + halfsize),
                         BAR_WIDTH, 'Black')

    def drawo(self, canvas, pos):
        """
        Draw an O on the given canvas at the given position.
        """
        halfsize = .4 * self._bar_spacing
        canvas.draw_circle(pos, halfsize, BAR_WIDTH, 'Black')

    # to be done
    def drawValidRegion(self, boxrow, boxcol):
        pass

    def draw(self, canvas):
        """
        Updates the tic-tac-toe GUI.
        """
        # Draw the thin line
        for bar_start in range(self._bar_spacing,
                               GUI_WIDTH - 1,
                               self._bar_spacing):
            
            numbar = bar_start // self._bar_spacing
            if numbar == self._size * self._size:
                continue
            if numbar % (self._size) == 0:
                continue
            # barw = ((numbar % (self._size) == 0 ) + 1) * BAR_WIDTH
            barw = BAR_WIDTH * 0.5
            color = "Brown"
            # if numbar % (self._size) == 0 :
            #     color = "Black"
            canvas.draw_line((bar_start, 0),
                             (bar_start, GUI_HEIGHT),
                             barw,
                             color)
            canvas.draw_line((0, bar_start),
                             (GUI_WIDTH, bar_start),
                             barw,
                             color)
        
        # draw the heavy line
        for bar_start in range(self._bar_spacing,
                               GUI_WIDTH - 1,
                               self._bar_spacing):
            
            numbar = bar_start // self._bar_spacing
            if numbar == self._size * self._size:
                continue
            if numbar % (self._size) != 0:
                continue
            barw = BAR_WIDTH
            color = "Black"
            canvas.draw_line((bar_start, 0),
                             (bar_start, GUI_HEIGHT),
                             barw,
                             color)
            canvas.draw_line((0, bar_start),
                             (GUI_WIDTH, bar_start),
                             barw,
                             color)

        # Draw the current players' moves
        for boxrow in range(self._size):
            for boxcol in range(self._size):
                for row in range(self._size):
                    for col in range(self._size):
                        symbol = self._board.square(boxrow, boxcol, row, col)
                        coords = self.get_coords_from_grid(boxrow, boxcol, row, col)
                        if symbol == provided.PLAYERX:
                            self.drawx(canvas, coords)
                        elif symbol == provided.PLAYERO:
                            self.drawo(canvas, coords)

        # Run AI, if necessary
        if not self._wait:
            self.aimove()
        else:
            self._wait = False

    def click(self, position):
        """
        Make human move.
        """
        if self._inprogress and (self._turn == self._humanplayer):
            boxrow, boxcol, row, col = self.get_grid_from_coords(position)
            if self._board.square(boxrow, boxcol, row, col) == provided.EMPTY and (boxrow, boxcol, row, col) in self._board.get_valid_moves():
                self._board.move(boxrow, boxcol, row, col, self._humanplayer)
                self._turn = self._aiplayer
                winner = self._board.check_win()
                if winner is not None:
                    self.game_over(winner)
                self._wait = True

    def aimove(self):
        """
        Make AI move.
        """
        if self._inprogress and (self._turn == self._aiplayer):
            boxrow, boxcol, row, col = self._aifunction(self._board,
                                                        self._aiplayer,
                                                        self._parameter) # function parameter
            if self._board.square(boxrow, boxcol, row, col) == provided.EMPTY:
                self._board.move(boxrow, boxcol, row, col, self._aiplayer)
            self._turn = self._humanplayer
            winner = self._board.check_win()
            if winner is not None:
                self.game_over(winner)
            ### add here to highlight the effective region using self.boxrow_valid and  self.boxcol_valid
            self.boxrow_valid, self.boxcol_valid = boxrow, boxcol
            ### highlight the valid region
            self.drawValidRegion(boxrow, boxcol)

    def game_over(self, winner):
        """
        Game over
        """
        # Display winner
        if winner == provided.DRAW:
            self._label.set_text("It's a tie!")
        elif winner == provided.PLAYERX:
            self._label.set_text("X Wins!")
        elif winner == provided.PLAYERO:
            self._label.set_text("O Wins!")

            # Game is no longer in progress
        self._inprogress = False

    def get_coords_from_grid(self, boxrow, boxcol, row, col):
        """
        Given a grid position in the form (row, col), returns
        the coordinates on the canvas of the center of the grid.
        """
        # X coordinate = (bar spacing) * (col + 1/2)
        # Y coordinate = height - (bar spacing) * (row + 1/2)
        col = boxcol * self._size + col
        row = boxrow * self._size + row
        return (self._bar_spacing * (col + 1.0 / 2.0),  # x
                self._bar_spacing * (row + 1.0 / 2.0))  # y

    def get_grid_from_coords(self, position):
        """
        Given coordinates on a canvas, gets the indices of
        the grid.
        """
        posx, posy = position
        r = posy // self._bar_spacing
        c = posx // self._bar_spacing
        boxrow = r // self._size
        boxcol = c // self._size
        row = r % self._size
        col = c % self._size
        return (boxrow,
                boxcol,
                row,
                col)


def run_gui(board_size, ai_player, ai_function, ntrials, reverse=False):
    """
    Instantiate and run the GUI
    """
    gui = TicTacGUI(board_size, ai_player, ai_function, ntrials, reverse)
    gui.start()