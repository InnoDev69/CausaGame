from src.core.game import Game

def main():
    game = Game()
    game.load_map("src/world/map.txt")
    game.run()

if __name__ == "__main__":
    main()