import pygame
import random
import config

class Snake:
    def __init__(self):
        self.w = 10
        self.h = 10
        self.x = config.game_width / 2
        self.y = config.game_height / 2
        self.x_new = self.x
        self.y_new = self.y
        self.color = (60, 60, 60)
        self.speed = 10
        self.score = 0
        self.x_change = 0
        self.y_change = 0
        self.pre_direction = None
        self.direction = random.randint(0, 3)
        self.body = []

    def Eat(self):
        self.score += 1

    def draw(self, display):
        pygame.draw.rect(display, color=self.color, rect=[self.x, self.y, self.w, self.h])
        for index, item in enumerate(self.body):
            if index % 2 == 0:
                pygame.draw.rect(display, color=(120,120,120), rect=[item[0], item[1], self.w, self.h])
            else:
                pygame.draw.rect(display, color=(60, 60, 60), rect=[item[0], item[1], self.w, self.h])

    def move(self):
        if self.direction == 0:
            self.x_change = -1
            self.y_change = 0

        elif self.direction == 1:
            self.x_change = 1
            self.y_change = 0

        elif self.direction == 2:
            self.x_change = 0
            self.y_change = -1

        elif self.direction == 3:
            self.x_change = 0
            self.y_change = 1

        self.body.append([self.x, self.y])
        if len(self.body) > self.score:
            del (self.body[0])

        self.x += self.x_change * self.speed
        self.y += self.y_change * self.speed

    def collision_with_body(self, direction):
        for part in self.body:
            if direction == 0:
                if abs(self.x - part[0]) < 10 and abs(self.y + 10 - part[1]) == 0:
                    return True
                if abs(self.x - part[0]) == 0 and abs(self.y + 10 - part[1]) < 10:
                    return True

            if direction == 1:
                if abs(self.x + 10 - part[0]) < 10 and abs(self.y - part[1]) == 0:
                    return True
                if abs(self.x + 10 - part[0]) == 0 and abs(self.y - part[1]) < 10:
                    return True

            if direction == 2:
                if abs(self.x - 10 - part[0]) < 10 and abs(self.y - part[1]) == 0:
                    return True
                if abs(self.x - 10 - part[0]) == 0 and abs(self.y - part[1]) < 10:
                    return True

            if direction == 3:
                if abs(self.x - part[0]) < 10 and abs(self.y - 8 - part[1]) == 0:
                    return True
                if abs(self.x - part[0]) == 0 and abs(self.y - 10 - part[1]) < 10:
                    return True

        return False

    def collision_with_wall(self, direction):
        if direction == 2:
            if self.y - 10 > config.wall_offset:
                return False

        elif direction == 1:
            if self.x + 10 < config.game_width - config.wall_offset:
                return False

        elif direction == 3:
            if self.y + 10 < config.game_height - config.wall_offset:
                return False

        elif direction == 0:
            if self.x - 10 > config.wall_offset:
                return False

        return True

    def vision(self, apple):
        # left
        if self.x > apple.x and self.y == apple.y:
            for part in self.body:
                if self.x > part[0] > apple.x and self.y == part[1]:
                    break
            else:
                return '0'

        # left up
        if abs(self.x - apple.x) == abs(self.y - apple.y) and self.x > apple.x and self.y > apple.y:
            for part in self.body:
                if abs(self.x - part[0]) == abs(self.y - part[1]) and self.x > part[0] > apple.x and self.y > part[1] > apple.y:

                    break
            else:
                return '02'

        # right
        if self.x < apple.x and self.y == apple.y:
            for part in self.body:
                if self.x < part[0] < apple.x and self.y == part[1]:
                    break
            else:
                return '1'

        # down right
        if abs(self.x - apple.x) == abs(self.y - apple.y) and self.x < apple.x and self.y < apple.y:
            for part in self.body:
                if abs(self.x - part[0]) == abs(self.y - part[1]) and self.x < part[0] < apple.x and self.y < part[1] < apple.y:

                    break
            else:
                return '31'

        # up
        if self.x == apple.x and self.y > apple.y:
            for part in self.body:
                if self.x == part[0] and self.y > part[1] > apple.y:
                    break
            else:
                return '2'

        # up right
        if abs(self.x - apple.x) == abs(self.y - apple.y) and self.x < apple.x and self.y > apple.y:
            for part in self.body:
                if abs(self.x - part[0]) == abs(self.y - part[1]) and self.x < part[0] < apple.x and self.y > part[1] > apple.y:
                    break
            else:
                return '21'

        # down
        if self.x == apple.x and self.y < apple.y:
            for part in self.body:
                if self.x == part[0] and self.y < part[1] < apple.y:
                    break
            else:
                return '3'

        # down left
        if abs(self.x - apple.x) == abs(self.y - apple.y) and self.x > apple.x and self.y < apple.y:
            for part in self.body:
                if abs(self.x - part[0]) == abs(self.y - part[1]) and self.x > part[0] > apple.x and self.y < part[1] < apple.y:
                    break
            else:
                return '30'

        return None

    def decision(self, direction):
        # left
        if direction == '0':
            if self.direction != 1:
                self.direction = 0

        # up left
        elif direction == '02':
            if self.direction != 1:
                self.direction = 0
            elif self.direction != 3:
                self.direction = 2

        # right
        elif direction == '1':
            if self.direction != 0:
                self.direction = 1

        # down right
        elif direction == '31':
            if self.direction != 0:
                self.direction = 1
            elif self.direction != 2:
                self.direction = 3

        # up
        elif direction == '2':
            if self.direction != 3:
                self.direction = 2

        # up right
        elif direction == '21':
            if self.direction != 3:
                self.direction = 2
            elif self.direction != 0:
                self.direction = 1

        # down
        elif direction == '3':
            if self.direction != 2:
                self.direction = 3

        # down left
        elif direction == '30':
            if self.direction != 2:
                self.direction = 3
            elif self.direction != 1:
                self.direction = 0

