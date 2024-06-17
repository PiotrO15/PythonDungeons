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

        if pressed[pygame.K_e]:
            ...
            # interact with objects

        speed_adj = self.speed * self.game.dt

        # Define velocity for each direction
        vel_y = (pressed[pygame.K_s] - pressed[pygame.K_w])
        vel_x = (pressed[pygame.K_d] - pressed[pygame.K_a])
        velocity = pygame.math.Vector2(vel_x, vel_y)
        if velocity.length() != 0:
            velocity.normalize_ip()
            velocity.scale_to_length(speed_adj)

        self.set_velocity(velocity)


    def update(self) -> None:
        if self.dead:
            self.game.paused = True
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
        for entry in self.game.current_room.doors:
            if entry.rect.collidepoint(self.hitbox.midbottom):
                previous_room_position = self.game.current_room.position

                # Change room
                self.game.current_room = self.game.dungeon[entry.destination]
                while self.game.current_room.master:
                    self.game.current_room = self.game.dungeon[self.game.current_room.master]

                # Find the door that leads to the previous room
                for door in self.game.current_room.doors:
                    # find destination of the door
                    destination = door.destination
                    while self.game.dungeon[destination].master:
                        destination = self.game.dungeon[destination].master

                    # if the door leads to previous room, appear next to it
                    if destination == previous_room_position:
                        room = self.game.current_room
                        # Calculate the new player position based on the door position
                        room_size_px = (room.size[0] * utils.ROOM_DIMENSIONS[0] * utils.TILE_SIZE, room.size[1] * utils.ROOM_DIMENSIONS[1] * utils.TILE_SIZE)
                        top_left_corner = [(a - b)/2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]

                        # Add offset so the player stays inside the room
                        door_y, door_x = door.coords
                        if door_y == 0:
                            self.rect.x = top_left_corner[0] + door_x * utils.TILE_SIZE
                            self.rect.y = top_left_corner[1] + (door_y + 1) * utils.TILE_SIZE
                        elif door_y == (room.size[1] * utils.ROOM_DIMENSIONS[1] - 1):
                            self.rect.x = top_left_corner[0] + door_x * utils.TILE_SIZE
                            self.rect.y = top_left_corner[1] + (door_y - 1) * utils.TILE_SIZE
                        elif door_x == 0:
                            self.rect.x = top_left_corner[0] + (door_x + 1) * utils.TILE_SIZE
                            self.rect.y = top_left_corner[1] + door_y * utils.TILE_SIZE
                        elif door_x == (room.size[0] * utils.ROOM_DIMENSIONS[0] - 1):
                            self.rect.x = top_left_corner[0] + (door_x - 1) * utils.TILE_SIZE
                            self.rect.y = top_left_corner[1] + door_y * utils.TILE_SIZE
                break

    def calculate_damage(self, enemy):
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


