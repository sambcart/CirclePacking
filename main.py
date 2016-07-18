import sys
import time
import pygame

from tree import Tree

def handle_cli_input(default_kwargs):
	kwargs = default_kwargs.copy()

	try:
		for key, val in map(lambda f_arg: f_arg.split("="), sys.argv[1:]):
			assert(key in default_kwargs.keys())
			kwargs[key] = eval(val)

	except (TypeError, AssertionError, ValueError):
		print "Bad uage, using default values."
		kwargs = default_kwargs.copy()

	return kwargs

def main():
	default_kwargs = {
		"size": 8000,
		"rad": 200,
		"boundary_rad": 3200,
		"rand_var": 0.3,
		"rand_mean": 0.92,
		"rad_lower_lim": 13
	}

	kwargs = handle_cli_input(default_kwargs)
	SIZE = kwargs["size"]

	screen = pygame.Surface((SIZE, SIZE))
	screen.fill((45,45,45))

	t = Tree(**kwargs)
	t.build(60)
	t.draw_triangles(screen, (255,255,255), filled=True, aalias=True)
	pygame.image.save(screen, "circle-genart-{}.png".format(int(time.time())))

if __name__ == "__main__":
	main()
