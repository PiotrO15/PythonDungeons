import math

import pygame
from math import sqrt
from src.entities.entity import Entity
from src import utils
from src.utils import time_passed


class Player(Entity):
    name = 'player'
    speed = 300
    max_hp = 100
    hp = max_hp
    base_attack = 40
    gold = 0
    shield = 0
    strength = 1

    def __init__(self, game):
        Entity.__init__(self, game, self.name)
        self.center()
        self.weapon = None
        self.attack_cooldown = 0

    def input(self):
        pressed = pygame.key.get_pressed()

        speed_adj = self.speed * self.game.dt

        # Define velocity for each direction
        vel_y = (pressed[pygame.K_s] - pressed[pygame.K_w])
        vel_x = (pressed[pygame.K_d] - pressed[pygame.K_a])
        velocity = pygame.math.Vector2(vel_x, vel_y)
        if velocity.length() != 0:
            velocity.normalize_ip()
            velocity.scale_to_length(speed_adj)

        self.set_velocity(velocity)

        # if pressed[pygame.K_SPACE] and self.can_attack():
        if pygame.mouse.get_pressed()[0] and self.can_attack():
            self.attack()


    def update(self) -> None:
        if self.dead:
            self.game.paused = True
            return

        self.check_collisions()
        if self.can_move:
            self.rect.move_ip(*self.velocity)
            self.hitbox.move_ip(*self.velocity)

        self.detect_death()

        self.update_hitbox()

    def center(self):
        self.rect = self.image[0].get_rect(center=(self.game.display.get_width() / 2, self.game.display.get_height() / 2))

    def use_door(self, door):
        previous_room_position = self.game.current_room.position

        # Change room
        self.game.current_room = self.game.dungeon[door.destination]
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
                room_size_px = (room.size[0] * utils.ROOM_DIMENSIONS[0] * utils.TILE_SIZE,
                                room.size[1] * utils.ROOM_DIMENSIONS[1] * utils.TILE_SIZE)
                top_left_corner = [(a - b) / 2 for a, b in zip(utils.SCREEN_SIZE, room_size_px)]

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

    def can_attack(self):
        if time_passed(self.attack_cooldown, 300):
            self.attack_cooldown = pygame.time.get_ticks()
            return True

    def attack(self):

        # Attack area dimensions
        attack_width, attack_height = 120, 60

        # Calculate the angle of the attack rectangle based on mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dir_vector = pygame.math.Vector2(self.hitbox.x - mouse_x,
                                         self.hitbox.y - mouse_y)
        dir_vector.scale_to_length(1)
        angle = math.degrees(math.atan2(dir_vector.y, dir_vector.x))

        # Calculate the angle of the attack rectangle based on the player's velocity (unused)
        # angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x))


        attack_rect = pygame.Rect(0, 0, attack_width, attack_height)

        # Position the attack rectangle relative to the player's position
        attack_rect.center = self.hitbox.center
        attack_rect.centerx -= int(dir_vector.x * 40)
        attack_rect.centery -= int(dir_vector.y * 40)

        # Rotate the attack rectangle
        attack_surface = pygame.Surface((attack_width, attack_height), pygame.SRCALPHA)
        attack_surface.fill((255, 0, 0, 128))  # Semi-transparent red for visualization
        attack_surface = pygame.transform.rotate(attack_surface, -angle)
        attack_rect = attack_surface.get_rect(center=attack_rect.center)

        # Draw attack rectangle for visualization
        # self.game.display.blit(attack_surface, attack_rect.topleft)

        # Handle collision with enemies
        for enemy in self.game.current_room.enemy_list:
            if attack_rect.colliderect(enemy.hitbox):
                enemy.hp -= self.strength * self.base_attack

    def calculate_damage(self, enemy):
        if not self.shield and not self.dead:
            self.hp = max(0, self.hp - enemy.damage)
            #TODO hurt sound / animation?
            if not self.dead:
                self.hurt = True
        elif self.shield:
            self.shield -= 1
