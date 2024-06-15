import random

from src.entities.enemy import Enemy, EnemyT1

class EnemyManager:
    def __init__(self, game):
        self.game = game
        self.damage_multiplier = 1
        self.health_multiplier = 1

    def draw_enemies(self, surface):
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
                    enemy = EnemyT1(self.game, random.randint(100, 150) / 10, room)
                    self.upgrade_enemy(enemy)
                    room.enemy_list.append(enemy)
                    room.enemy_list[-1].spawn()

    def upgrade_enemy(self, enemy):
        enemy.damage *= self.damage_multiplier
        enemy.max_hp *= self.health_multiplier
        enemy.hp *= self.health_multiplier

