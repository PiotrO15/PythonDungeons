import pygame
from math import sqrt
from src.entities.entity import Entity
from src import utils


class Player(Entity):
    name = 'player'
    speed = 300
    max_hp = 100
    hp = max_hp
    gold = 0
    shield = 0
    strength = 1
    items = []

    def __init__(self, game):
        Entity.__init__(self, game, self.name)
        self.center()
        self.weapon = None
        self.attack_cooldown = 350  # ms

    def input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_e] and pygame.time.get_ticks() - self.time > 300:
            self.time = pygame.time.get_ticks()
            # interact with objects

        speed_adj = self.speed * self.game.dt

        # Define velocity for each direction
        vel_y = (pressed[pygame.K_s] - pressed[pygame.K_w])
        vel_x = (pressed[pygame.K_d] - pressed[pygame.K_a])
        velocity = pygame.math.Vector2(vel_x, vel_y)
        if velocity.length() != 0:
            velocity.normalize_ip()
            velocity.scale_to_length(speed_adj)
        # print(vel)
        self.set_velocity(velocity)


    def update(self) -> None:
        if self.dead:
            return
        self.wall_collision()
        if self.can_move:
            self.rect.move_ip(*self.velocity)
            self.hitbox.move_ip(*self.velocity)
        self.use_door()
        self.detect_death()

        self.update_hitbox()

    def center(self):
        self.rect = self.image.get_rect(center=(self.game.display.get_width() / 2, self.game.display.get_height() / 2))

    def use_door(self):
        screen_surface = self.game.display

        for entry in self.game.current_room.doors_rect:
            if entry['rect'].collidepoint(self.hitbox.midbottom):
                previous_room_position = self.game.current_room.position
                previous_room_size = self.game.current_room.size
                self.game.current_room = self.game.dungeon[entry['destination']]
                while self.game.current_room.master:
                    self.game.current_room = self.game.dungeon[self.game.current_room.master]

                # Find the door that leads to the previous room
                for door in self.game.current_room.doors.items():
                    if (previous_room_position[0] <= door[1][0] <= previous_room_position[0] + previous_room_size[0] - 1
                            and previous_room_position[1] <= door[1][1] <= previous_room_position[1] + previous_room_size[1] - 1):
                        room = self.game.current_room
                        # Calculate the new player position based on the door position
                        room_size_px = (room.size[0] * utils.ROOM_DIMENSIONS[0] * utils.TILE_SIZE, room.size[1] * utils.ROOM_DIMENSIONS[1] * utils.TILE_SIZE)
                        top_left_corner = [(a - b)/2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]
                        # Add offset so the player stays inside the room
                        if door[0][0] == 0:
                            self.rect.x = top_left_corner[0] + door[0][1] * utils.TILE_SIZE
                            self.rect.y = top_left_corner[1] + (door[0][0] + 1) * utils.TILE_SIZE
                        elif door[0][0] == (room.size[1] * utils.ROOM_DIMENSIONS[1] - 1):
                            self.rect.x = top_left_corner[0] + door[0][1] * utils.TILE_SIZE
                            self.rect.y = top_left_corner[1] + (door[0][0] - 1) * utils.TILE_SIZE
                        elif door[0][1] == 0:
                            self.rect.x = top_left_corner[0] + (door[0][1] + 1) * utils.TILE_SIZE
                            self.rect.y = top_left_corner[1] + door[0][0] * utils.TILE_SIZE
                        elif door[0][1] == (room.size[0] * utils.ROOM_DIMENSIONS[0] - 1):
                            self.rect.x = top_left_corner[0] + (door[0][1] - 1) * utils.TILE_SIZE
                            self.rect.y = top_left_corner[1] + door[0][0] * utils.TILE_SIZE
                break

    def calculate_collision(self, enemy):
        if not self.shield and not self.dead:
            self.hp = max(0, self.hp - enemy.damage)
            #TODO hurt sound / animation?
            if not self.dead:
                self.hurt = True
        elif self.shield:
            self.shield -= 1

    def draw(self, surface):
        if self.dead:
            return
        surface.blit(self.image, self.rect)


