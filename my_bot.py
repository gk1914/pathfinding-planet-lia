import asyncio

from core.bot import Bot
from core.networking_client import connect
from core.enums import Direction

from my_priority import Tile
from A_star import AStar
from utils import future


# Example Python 3 bot implementation for Planet Lia Bounce Evasion.
class MyBot(Bot):

    # Called only once before the match starts. It holds the
    # data that you may need before the game starts.
    def setup(self, initial_data):
        self.initial_data = initial_data

    # Called repeatedly while the match is generating. Each
    # time you receive the current match state and can use
    # response object to issue your commands.
    def update(self, state, response):
        # prepare data
        player_pos = Tile(self.initial_data["map"], state["yourUnit"]["x"], state["yourUnit"]["y"])
        enemy_pos = Tile(self.initial_data["map"], state["opponentUnit"]["x"], state["opponentUnit"]["y"])
        c1 = Tile(self.initial_data["map"], state["coins"][0]["x"], state["coins"][0]["y"])
        c2 = Tile(self.initial_data["map"], state["coins"][1]["x"], state["coins"][1]["y"])

        # get closest (and most optimal) coin to be "chased"
        dist1 = player_pos.evaluate(c1)
        dist2 = player_pos.evaluate(c2)
        enemy_dist1 = enemy_pos.evaluate(c1)
        enemy_dist2 = enemy_pos.evaluate(c2)
        if enemy_dist1 <= enemy_dist2:
            enemy_closest = c1
        else:
            enemy_closest = c2
        if dist1 <= dist2 and (enemy_closest.is_same(c1) and enemy_dist1 < dist1):
            closest_coin = c2
        elif dist2 <= dist1 and (enemy_closest.is_same(c2) and enemy_dist2 < dist2):
            closest_coin = c1
        elif dist1 <= dist2:
            closest_coin = c1
        else:
            closest_coin = c2

        # A* pathfinding
        astar = AStar(self.initial_data["map"], player_pos, closest_coin, state)
        path = astar()
        while path.parent:
            if path.parent.id != (player_pos.X, player_pos.Y):
                path = path.parent
            else:
                break

        if player_pos.X - path.X == 1:
            direction = Direction.LEFT
        elif player_pos.X - path.X == -1:
            direction = Direction.RIGHT
        elif player_pos.Y - path.Y == -1:
            direction = Direction.UP
        else:
            direction = Direction.DOWN

        # get list of all saw positions in the next update
        saw_positions = future(state["saws"], self.initial_data["map"])

        # check if player collides with saw in the next update
        dodge = False
        for s in saw_positions:
            if s == (path.X, path.Y):
                dodge = True

        # move if not about to collide
        if not dodge:
            response.move_unit(direction)


# Connects your bot to match generator, don't change it.
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect(MyBot()))
