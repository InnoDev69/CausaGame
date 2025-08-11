from src.core.game import Game

def main():
    game = Game()
    game.build_world()
    game.run()

if __name__ == "__main__":
    main()