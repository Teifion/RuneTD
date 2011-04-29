from game import rune
import sys

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == 'test':
		raise Exception("Test mode not yet implimented")
	else:
		r = rune.Rune_game()
		r.start()
