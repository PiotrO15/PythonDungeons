import random

from python_dungeons.entities.enemy import ReaperSkeleton, FighterSkeleton


class EnemyManager:
    def __init__(self, game):
        self.game = game
        self.damage_multiplier = 1
        self.health_multiplier = 1

    def draw_enemies(self):
        for enemy in self.game.current_room.enemy_list:
            enemy.draw()

    def update_enemies(self):
        for enemy in self.game.current_room.enemy_list:
            enemy.update()

    def add_enemies(self):
        for row in self.game.dungeon:
            for room in row:
                level = self.game.level

                num_of_enemies = random.randint(0, 1 + level * room.size[0] * room.size[1])
                for _ in range(num_of_enemies):
                    if random.random() < 0.5:
                        enemy = ReaperSkeleton(self.game, random.randint(100, 150), room)
                    else:
                        enemy = FighterSkeleton(self.game, random.randint(100, 150), room)
                    self.upgrade_enemy(enemy)
                    room.enemy_list.append(enemy)
                    room.enemy_list[-1].spawn()

    def upgrade_enemy(self, enemy):
        enemy.damage *= self.damage_multiplier
        enemy.max_hp *= self.health_multiplier
        enemy.hp *= self.health_multiplier
