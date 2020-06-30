class Game:

    def __init__(self, maze_id):
        self.maze_id = maze_id

    @staticmethod
    def create(maze_id: str):
        return Game(maze_id)

    def player_count(self):
        return 1