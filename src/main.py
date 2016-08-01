import sys
import time
import pygame

from pygame.locals import *

from tree import Tree

def handle_cli_input(default_kwargs):
    kwargs = default_kwargs.copy()

    try:
        f_args = map(lambda f_arg: f_arg.split("="), sys.argv[1:])
        for key, val in f_args:
            assert key in default_kwargs.keys()
            kwargs[key] = eval(val)

    except (TypeError, AssertionError, ValueError):
        print "Bad usage, using default values."
        kwargs = default_kwargs.copy()

    return kwargs

def main():
    default_kwargs = {
        "size": 8000,
        "rad": 240,
        "boundary_rad": None,
        "rand_var": 0.04,
        "rand_mean": 0.98,
        "rad_lower_lim": 12
    }

    small_kwargs = {
        "size": 800,
        "rad": 2,
        "boundary_rad": None,
        "rand_var": 0.04,
        "rand_mean": 0.98,
        "rad_lower_lim": 2
    }

    kwargs = handle_cli_input(default_kwargs)
    #kwargs = handle_cli_input(small_kwargs)
    size = kwargs["size"]

    screen = pygame.Surface((size, size))
    #screen = pygame.display.set_mode((size, size))
    screen.fill((255, 255, 255))

    tree = Tree(**kwargs)
    tree.build_LIFO()
    tree.draw_triangles(screen, (45, 45, 45), filled=True, aalias=True)

    pygame.image.save(screen, "pics/circle-genart-{}.png".format(int(time.time())))

    sys.exit()

    """
    tree.build_LIFO_draw(screen, (45, 45, 45), filled=True, aalias=True)
    tree.build_FIFO_draw(screen, (45, 45, 45), filled=True, aalias=True)

    while True:
        for event in pygame.event.get(QUIT):
            sys.exit()
        pygame.display.update()
    """

if __name__ == "__main__":
    main()
