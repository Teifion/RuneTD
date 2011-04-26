import rune_engine, rune_game
import sys

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == 'test':
		raise Exception("Test mode not yet implimented")
	else:
		r = rune_engine.Rune_engine(rune_game.Rune_game())
		r.start()
