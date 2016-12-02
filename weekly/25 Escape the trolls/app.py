import random, time, sys

# key catching code
import sys,tty,termios
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
# end key catching code

maze = '''#########################################################################
#   #               #               #           #                   #   #
#   #   #########   #   #####   #########   #####   #####   #####   #   #
#               #       #   #           #           #   #   #       #   #
#########   #   #########   #########   #####   #   #   #   #########   #
#       #   #               #           #   #   #   #   #           #   #
#   #   #############   #   #   #########   #####   #   #########   #   #
#   #               #   #   #       #           #           #       #   #
#   #############   #####   #####   #   #####   #########   #   #####   #
#           #       #   #       #   #       #           #   #           #
#   #####   #####   #   #####   #   #########   #   #   #   #############
#       #       #   #   #       #       #       #   #   #       #       #
#############   #   #   #   #########   #   #####   #   #####   #####   #
#           #   #           #       #   #       #   #       #           #
#   #####   #   #########   #####   #   #####   #####   #############   #
#   #       #           #           #       #   #   #               #   #
#   #   #########   #   #####   #########   #   #   #############   #   #
#   #           #   #   #   #   #           #               #   #       #
#   #########   #   #   #   #####   #########   #########   #   #########
#   #       #   #   #           #           #   #       #               #
#   #   #####   #####   #####   #########   #####   #   #########   #   #
#   #                   #           #               #               #   #
# X #####################################################################'''

game_won = False

def get_maze_width():
    return len(maze.splitlines()[0])

def get_maze_height():
    return len(maze.splitlines())

def replace_character(x, y, character):
    '''
    Replace character on the map
    '''
    global maze

    i = 0
    j = 0

    temporary_maze = list(maze)

    for c in range(0, len(temporary_maze)):
        if (temporary_maze[c] == '\n'):
            j += 1
            i = 0

            continue

        if ((i == x) and (j == y)):
            temporary_maze[c] = character
            maze = ''.join(temporary_maze)

            break
        else:
            i += 1

def check_for_obstacle(x, y):
    '''
    Return whether there is an obstacle at the location on the map
    '''
    global game_won

    is_obstacle = False

    if ((x < 0) or (x > get_maze_width() - 1) or (y < 0) or (y > get_maze_height() - 1)):
        is_obstacle = True
    elif (maze.splitlines()[y][x] == 'X'):
        game_won = True
    elif (maze.splitlines()[y][x] != ' '):
        is_obstacle = True

    return is_obstacle

def obstacle_found(x, y, direction):
    '''
    Return whether there is an obstacle in the direction the player is intending to move
    '''
    intended_x = x
    intended_y = y

    if (direction == 'u'):
        intended_y -= 1
    elif (direction == 'd'):
        intended_y += 1
    elif (direction == 'l'):
        intended_x -= 1
    elif (direction == 'r'):
        intended_x += 1

    return check_for_obstacle(intended_x, intended_y)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_up(self):
        if (not obstacle_found(self.x, self.y, 'u')):
            replace_character(self.x, self.y, ' ')
            replace_character(self.x, self.y - 1, '^')

            self.y -= 1
        else:
            replace_character(self.x, self.y, '^')

    def move_down(self):
        if (not obstacle_found(self.x, self.y, 'd')):
            replace_character(self.x, self.y, ' ')
            replace_character(self.x, self.y + 1, 'v')

            self.y += 1
        else:
            replace_character(self.x, self.y, 'v')

    def move_left(self):
        if (not obstacle_found(self.x, self.y, 'l')):
            replace_character(self.x, self.y, ' ')
            replace_character(self.x - 1, self.y, '<')

            self.x -= 1
        else:
            replace_character(self.x, self.y, '<')

    def move_right(self):
        if (not obstacle_found(self.x, self.y, 'r')):
            replace_character(self.x, self.y, ' ')
            replace_character(self.x + 1, self.y, '>')

            self.x += 1
        else:
            replace_character(self.x, self.y, '>')

def spawn_player():
    '''
    Spawn player on map
    '''
    maze_width = get_maze_width()
    maze_height = get_maze_height()

    while True:
        x = random.randrange(maze_width)
        y = random.randrange(maze_height)

        if (not check_for_obstacle(x, y)):
            player = Player(x, y)

            replace_character(player.x, player.y, '^')

            return player

def show_map():
    '''
    Show the map
    '''
    print()
    print(maze)

def play(player):
    '''
    Main game function
    '''
    show_map()

    # key catching code
    inkey = _Getch()
    while(1):
            k=inkey()
            if k!='':
                break
    key = ord(k)
    # end key catching code

    if key == 32:
        sys.exit()
    elif key == 65: # up arrow
        player.move_up()
    elif key == 66: # down arrow
        player.move_down()
    elif key == 68: # left arrow
        player.move_left()
    elif key == 67: # right arrow
        player.move_right()

def init():
    '''
    Initialize player object and start main game loop
    '''
    player = spawn_player()

    while (not game_won):
        play(player)

    print("Congrats! You won!")

init()
