# Snake for the Card10
# 22.8.2019
# Jan Fecht

import vibra # vibrate when dying
import urandom # random food gen
import utime
import buttons
import color
import display

game_width = 32
game_height = 16
num_start_tiles = 4
sleep_time_ms = 100
snake_col = color.GREEN
food_col = color.RED
bg_col = color.BLACK

physical_width = 160
physical_height = 80
tile_width = physical_width // game_width
tile_height = physical_height // game_height

class Direction:
    UP = (0,-1)
    LEFT = (-1,0)
    RIGHT = (1,0)
    DOWN = (0,1)
    clockwise = [UP, RIGHT, DOWN, LEFT]
    def __init__(self, direction=LEFT):
        self.direction = direction

    def turn_clockwise(self):
        self.direction = self.clockwise[(self.clockwise.index(self.direction) + 1) % 4]

    def turn_counterclockwise(self):
        self.direction = self.clockwise[(self.clockwise.index(self.direction) - 1) % 4]


class Game:
    def reset(self):
        self.pos = [(game_width // 2 + i, game_height // 2) for i in range(num_start_tiles)]
        self.tile_directions = [Direction.LEFT] * len(self.pos)
        self.direction = Direction(Direction.LEFT)
        self.grow = False
        #def is_valid_pos(p):
        #    x,y = p
        #    return 0 <= x < game_width and 0 <= y <= game_width 
        #assert(all[is_valid_pos(p) for p in self.pos])
        self.gen_new_food()

    def __init__(self):
        self.disp = display.open()
        self.disp.__enter__()
        self.reset()

    def __enter__(self):
        return self

    def __exit__ (self, t, value, tb):
        self.disp.__exit__()

    def gen_new_food(self):
        while True:
            self.food_pos = (urandom.randrange(0, game_width),
                             urandom.randrange(0, game_height))
            if self.food_pos not in self.pos:
                break


    def step(self, button):
        """
        returns True if not Dead
        """
        if button == buttons.BOTTOM_LEFT:
            self.direction.turn_counterclockwise()
        elif button == buttons.BOTTOM_RIGHT:
            self.direction.turn_clockwise()
        else:
            pass

        self.tile_directions.pop()
        self.tile_directions.insert(0,self.direction.direction)

        headx, heady = self.pos[0]
        if ((headx + self.direction.direction[0]) % game_width,
                (heady + self.direction.direction[1]) % game_height) in self.pos:
                return False


        last = self.pos[-1]
        for i in range(len(self.pos)):
            x, y = self.pos[i]
            deltax, deltay = self.tile_directions[i]
            self.pos[i] = ((x + deltax) % game_width, (y + deltay) % game_height)
        if self.grow:
            self.pos.append(last)
            self.tile_directions.append(self.tile_directions[-1])
            self.grow = False

        if self.food_pos in self.pos:
            self.gen_new_food()
            self.grow = True

        return True

    def draw(self):
        self.disp.clear()
        self.disp.rect(0, 0, physical_width, physical_height, col=bg_col)
        for (x,y) in self.pos:
            self.disp.rect(x*tile_width, y*tile_width, (x+1)*tile_width,
                    (y+1)*tile_height, col=snake_col)
        x,y = self.food_pos
        self.disp.rect(x*tile_width, y*tile_width, (x+1)*tile_width, (y+1)*tile_height, col=food_col)
        self.disp.update()

    def run(self):
        while True:
            self.draw()
            utime.sleep_ms(sleep_time_ms)
            b_pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT)
            alive = self.step(b_pressed)
            if not alive:
                vibra.vibrate(100)
                self.disp.rect(0, 0, physical_width, physical_height,
                        col=color.RED)
                self.disp.print("DED",bg=color.RED)
                self.disp.print("Length: {}".format(len(self.pos)),bg=color.RED,posy=30)
                self.disp.update()
                utime.sleep_ms(1000)
                buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT) # clear the queue
                while True:
                    b_pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT)
                    if b_pressed:
                        break
                break

def main():
    with Game() as g:
        while True:
            g.reset()
            g.run()


main()
