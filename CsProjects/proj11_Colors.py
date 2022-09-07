import math        # for sqrt
import random
from graphics import graphics

class Paint:
    """
        This class represents the drops of paint that fall into the lake.
        The drops each have a randomized color and will fall at a fixed
        velocity until colliding with the lake, at which point the drop
        will run the spread color method and destroy itself.

        The constructor stores info on the drop's column number, the size of
        the square for drawing, the random color rgb array, x and y positions,
        the grid of water square nodes, and finally the velocity that it
        travels downwards.
        Drop

        The class defines several helpful methods and fields:
            get_xy() returns x and y position for Game methods,
            offset correctly in a way that emulates a bottom collider
            get_radius() returns the size of the drop's collider,
            which is made smaller to only detect downwards.
            spread() is a recursive method that dilutes the colors
            of the drop and spreads them to the squares adjacent to each
            contact point. There is a limit to avoid the discoloration
            of default water colors, so that only the "paint" colors
            will spread.
            nearby() a game method used for detecting collisions with
            water squares. If the bottom collider is a cerain distance from
            a square collider, it will trigger
            move() moves the drop downwards each tick
            draw() draws the drop each tick
    """
    def __init__(self, spawn_column, square_size, rgb, grid):
        self._column = spawn_column
        self._size = square_size
        self._color = rgb
        self._x = square_size * spawn_column
        self._y = 0
        self._grid = grid
        self._velocity = 18

    def get_xy(self):
        offset_x = (self._size / 2 - (self._size/10))
        return (self._x + offset_x, self._y + self._size)

    def get_radius(self):
        return self._size / 4

    def spread(self, other):
        # The color of the drop is recursively "diluted"
        # each call so it forms a gradient
        diluted_color = [abs(other._color[0]), abs(other._color[1]),
                         abs(other._color[2])]
        max_rgb = max(diluted_color)
        min_rgb = min(diluted_color)
        # RGB Floors and Ceilings to limit "fading paint"
        # from reverting back to a darker color
        if (40 < other._color[0] < 120) and (140 < other._color[1] < 220) \
                and (180 < other._color[2] < 260):
            return
        # Prevents incorrect RGB values from passing
        if min_rgb > 10 and max_rgb < 250:
            other._color[0] -= 2
            other._color[1] -= 2
            other._color[2] -= 2
            other.get_adjacent(self._grid)
            for element in other._adjacent:
                if element is not None:
                    element._color = diluted_color
                    if element._down is not None and \
                            (max(element._color) < 250):
                        self.spread(element._down)
                        element._color = diluted_color

    def nearby(self, other, dist, game):
        pass
        bottom_collision = self._size / 4
        if dist < bottom_collision and type(other) == Water:
            other._color = self._color
            self.spread(other)
            for element in other._adjacent:
                if element is not None:
                    self.spread(element)
            game.remove_obj(self)

    def move(self, game):
        self._y += self._velocity

    def draw(self, win):
        color = win.get_color_string(self._color[0], self._color[1],
                                     self._color[2])
        win.rectangle(self._x, self._y, self._size, self._size, color)

class Water:
    """
        This class represents the Water squares that interact with the paint.
        Upon creation, each Water square's reference is stored on the grid so
        that adjacent water nodes can be linked. This allows for paint to
        spread between adjacent water particles. The water will fade to its
        default blue color over time, but paint can push down other paint and
        delay this process.

        The constructor stores info on the column and row number, collider
        size, rgb value, x and y position, paint decay rate, and each of the
        adjacent nodes (left, right, down)

        The class defines several helpful methods and fields:
            get_xy() returns properly offset origin point for water node
            collider
            get_radius() returns the size of the shape for collisions
            nearby() not used but included for game structure
            get_adjacent() returns the nodes to the left, right, and bottom of
            the instance as an array used inside the Paint's spread function.
            move() not used in this class, as the water does not move
            draw() returns each rgb value of the water back to the default
            of [80, 180, 220] by the decay rate each tick

    """
    def __init__(self, spawn_column, spawn_row, square_size, rgb, grid):
        self._column = spawn_column
        self._row = spawn_row - 7
        self._size = square_size
        self._color = rgb
        self._x = square_size * spawn_column
        self._y = square_size * spawn_row
        self._adjacent = []
        self._left = None
        self._right = None
        self._down = None
        self._decay = 2

    def get_xy(self):
        return (self._x + (self._size / 2), self._y + self._size / 2)

    def get_radius(self):
        return self._size

    def nearby(self, other, dist, game):
        pass

    def get_adjacent(self, grid):
        # Prevents Indexing errors, then searches grid to assign adjacent Nodes
        if self._column > 0:
            self._left = grid[self._column - 1][self._row]
        if self._column < 19:
            self._right = grid[self._column + 1][self._row]
        if self._row < 12:
            self._down = grid[self._column][self._row + 1]
        self._adjacent = [self._left, self._right, self._down]

    def move(self, game):
        pass

    def draw(self, win):
        # Returns water to default blue color ([80, 180, 220]) over time
        color = win.get_color_string(self._color[0], self._color[1],
                                     self._color[2])
        if self._color[0] < 80:
            self._color[0] += self._decay
        if self._color[0] > 80:
            self._color[0] -= self._decay
        if self._color[1] < 180:
            self._color[1] += self._decay
        if self._color[1] > 180:
            self._color[1] -= self._decay
        if self._color[2] < 220:
            self._color[2] += self._decay
        if self._color[2] > 220:
            self._color[2] -= self._decay
        win.rectangle(self._x, self._y, self._size, self._size, color)

class Game:
    def __init__(self, title, frame_rate, wid, hei):
        """Constructor.  Initializes the game to have zero objets; call
           add_obj() to add objects to the system.

           Parameters: the width and height of the window
        """
        self._wid = wid
        self._hei = hei

        self._frame_rate = frame_rate

        self._win = graphics(wid, hei, title)

        # this is a configuration setting - it changes how we calculate
        # the distance between objects in do_nearby_calls()
        self._account_for_radii_in_dist = False

        # the user must call add_obj() to add to this set
        self._active_objs = set()

        # see what remove_obj() and perform_moves() do, to understand this
        # variable.
        self._pending_removes = set()
        self._pending_adds    = set()

        # I plan to add a feature, where the user can mark the game as "over"
        self._game_over = False

    def config_set(self, param, val):
        """Function to set various config variables.  Right now, it only
           supports a single parameter; I might add more later.  Give the name
           of the parameter (as a string), then the value.

           Parmeters: config parameter to set, value

           Supported Config Options:
             "account_for_radii_in_dist" -> Boolean
        """
        if param == "account_for_radii_in_dist":
            self._account_for_radii_in_dist = val
        else:
            assert False   # unrecognized config parameter

    def set_game_over(self):
        self._game_over = True
    def is_over(self):
        return self._game_over


    def add_obj(self, new_obj):
        """Adds a new object to the game.  Can be called at any time, although
           if called in the middle of the nearby() or move() loops, it will not
           be added to the ongoing loop.  The object must implement the
           standard methods required of any object: get_xy(), get_radius(),
           nearby(), move(), and draw().

           Parameters: the new object
        """
        assert new_obj not in self._active_objs
        assert new_obj not in self._pending_adds
        self._pending_adds.add(new_obj)

    def remove_obj(self, bad_obj):
        """Queues up an object to be removed from the game.  It is
           permissible to call this multiple times on the same object during
           one clock tick; all of the removals will take place at once,
           *after* all of the nearby() and move() calls have been completed,
           but *before* any draw() calls.  It is illegal to call this if the
           object is not currently in the game.

           Arguments: object to remove
        """
        assert bad_obj in self._active_objs
        self._pending_removes.add(bad_obj)

    def _execute_adds_and_removes(self):
        """Helper function, used to handle common code in several of the
           primary game-loop functions.  Do not call directly.
        """
        self._active_objs -= self._pending_removes
        self._pending_removes = set()

        self._active_objs.update(self._pending_adds)
        self._pending_adds = set()

    def do_nearby_calls(self):
        """Figures out how close each object is to every other, sorts them by
           distance, and then performs all of the nearby() calls on the object
           pairs.  Makes all of the calls for a given "left-hand" object as a
           block; if the user returns False from any call, we terminate that
           inner loop, and then start delivering values for another left-hand
           value.

           Parameters: none
        """

        positions = []
        for o in self._active_objs:
            x, y = o.get_xy()
            positions.append( (o, x, y) )

        # Note that we're doing a 2D loop, but because we're only looking for
        # one version of each pair (not the reversed), notice that we do
        # something funny with the lower bound of the inner loop variable.
        distances = []
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                o1,x1,y1 = positions[i]
                o2,x2,y2 = positions[j]

                dist = math.sqrt( (x1-x2)**2 + (y1-y2)**2 )

                if self._account_for_radii_in_dist:
                    dist -= o1.get_radius()
                    dist -= o2.get_radius()

                # we add two records to the 'distances' array, so that we can
                # simply *sort* that list at the end.  Note that the way that
                # we arrange this, we will organize first by the left-hand
                # object, then by the distance, and then by the right-hand
                # object (the last of which will rarely be an issue)
                #
                # UPDATE: Note that I wanted to use object references here -
                #         but then I realized that we couldn't sort by those!
                #         so I need to use the indices into the positions[]
                #         array instead.
                distances.append( (i, dist, j) )
                distances.append( (j, dist, i) )


        # now that we're done *creating* the distances, we can sort all of
        # them.
        distances.sort()

        # there should be exactly n(n-1) elements in the array - since every
        # object in the game will be paired with n-1 others.
        n = len(positions)
        assert len(distances) == n*(n-1)

        # this loop is weird - but we have n different objects, each of which
        # has n-1 partners.  So I will implement each inner loop as looping
        # over a slice of the distances array.
        for i in range(n):
            for entry in distances[ (n-1)*i : (n-1)*(i+1) ]:
                k1,dist,k2 = entry
                assert k1 == i

                left  = positions[k1][0]
                right = positions[k2][0]

                # if the user returns False, then we will terminate this as a
                # left-hand element.
                if not left.nearby(right, dist, self):
                    break

    def do_move_calls(self):
        """Calls move() on every object in the game"""
        for o in self._active_objs:
            o.move(self)

    def draw(self):
        """Calls draw() on every object in the game.  Also does the rest of the
           misc calls necessary to animate the window.
        """

        # execute pending object changes (if any)
        self._execute_adds_and_removes()

        # if the window has been destroyed, then we will throw an exception when
        # we run clear() below.  So check for this condition first!
        if self._win.is_killed:
            self._game_over = True
            return

        self._win.clear()

        for o in self._active_objs:
            o.draw(self._win)

        self._win.update_frame(self._frame_rate)

def main():
    wid = 1200
    hei = 1200
    game = Game("Three Shapes", 30, wid, hei)
    game.config_set("account_for_radii_in_dist", True)
    grid = []
    spawn(game, wid, hei, grid)
    while not game.is_over():
        game.do_nearby_calls()
        game.do_move_calls()
        game.draw()
        spawn_drop(game, wid, hei, grid)


def spawn(game, wid, hei, grid):
    ''' This function creates the grid of water, then stores each of the game
        objects.
        The sizes are hardcoded for a balance of performance and fidelity
        Arguments: game: the game instance
        wid: the width of the canvas
        hei: the height of the canvas
        Return Values: None
        Pre-conditions: Canvas width and height must be created
    '''
    square_size = wid / 20
    rgb = [80, 180, 220]
    for x in range(0, 20):
        row_contents = []
        spawn_column = x
        for y in range(7, 20):
            spawn_row = y
            new_object = Water(spawn_column, spawn_row, square_size, rgb, grid)
            game.add_obj(new_object)
            row_contents += [new_object]
        grid += [row_contents]

def spawn_drop(game, wid, hei, grid):
    ''' This function spawns paint drops with random colors and at random
        column locations based on a random probability. It is called every
        game tick.
        The sizes are hardcoded for a balance of performance and fidelity
        Arguments: game: the game instance
        wid: the width of the canvas
        hei: the height of the canvas
        grid: the grid of Water nodes
        Return Values: None
        Pre-conditions: Canvas width and height must be created, grid must
        contain water nodes
    '''
    spawn_chance = random.randint(0, 100)
    if spawn_chance < 25:
        r = random.randint(30, 255)
        g = random.randint(30, 255)
        b = random.randint(30, 255)
        rgb = [r, g, b]
        square_size = wid / 20
        spawn_column = random.randint(0, 19)
        game.add_obj(Paint(spawn_column, square_size, rgb, grid))

main()