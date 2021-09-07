from argparse import ArgumentParser
import pygame
import numpy as np
from snake import Snake
from apple import Apple
import config
import tensorflow as tf


def get_data():
# distance-wall
    w0 = snake.x - config.wall_offset  # left
    w1 = config.game_width - config.wall_offset - snake.x  # right
    w2 = snake.y - config.wall_offset  # up
    w3 = config.game_height - config.wall_offset - snake.y  # down

# apple
    if snake.x == apple.x and snake.y > apple.y:
        a2 = abs(snake.x - apple.x) + abs(snake.y - apple.y)
    else:
        a2 = 0

    if abs(snake.x - apple.x) == abs(snake.y - apple.y) and snake.x < apple.x and snake.y > apple.y:
        a21 = abs(snake.x - apple.x) + abs(snake.y - apple.y)
    else:
        a21 = 0

    if snake.x < apple.x and snake.y == apple.y:
        a1 = abs(snake.x - apple.x) + abs(snake.y - apple.y)
    else:
        a1 = 0

    if abs(snake.x - apple.x) == abs(snake.y - apple.y) and snake.x < apple.x and snake.y < apple.y:
        a31 = abs(snake.x - apple.x) + abs(snake.y - apple.y)
    else:
        a31 = 0

    if snake.x == apple.x and snake.y < apple.y:
        a3 = abs(snake.x - apple.x) + abs(snake.y - apple.y)
    else:
        a3 = 0

    if abs(snake.x - apple.x) == abs(snake.y - apple.y) and snake.x > apple.x and snake.y < apple.y:
        a30 = abs(snake.x - apple.x) + abs(snake.y - apple.y)
    else:
        a30 = 0

    if snake.x > apple.x and snake.y == apple.y:
        a0 = abs(snake.x - apple.x) + abs(snake.y - apple.y)
    else:
        a0 = 0

    if abs(snake.x - apple.x) == abs(snake.y - apple.y) and snake.x > apple.x and snake.y > apple.y:
        a02 = abs(snake.x - apple.x) + abs(snake.y - apple.y)
    else:
        a02 = 0

# body

    for part in snake.body:
        if snake.x == part[0] and snake.y > part[1]:
            b2 = abs(snake.x - part[0]) + abs(snake.y - part[1])
            break
    else:
        b2 = 0

    for part in snake.body:
        if snake.x < part[0] and snake.y > part[1]:
            b21 = abs(snake.x - part[0]) + abs(snake.y - part[1])
            break
    else:
        b21 = 0

    for part in snake.body:
        if snake.x < part[0] and snake.y == part[1]:
            b1 = abs(snake.x - part[0]) + abs(snake.y - part[1])
            break
    else:
        b1 = 0

    for part in snake.body:
        if snake.x < part[0] and snake.y < part[1]:
            b31 = abs(snake.x - part[0]) + abs(snake.y - part[1])
            break
    else:
        b31 = 0

    for part in snake.body:
        if snake.x == part[0] and snake.y < part[1]:
            b3 = abs(snake.x - part[0]) + abs(snake.y - part[1])
            break
    else:
        b3 = 0

    for part in snake.body:
        if snake.x > part[0] and snake.y < part[1]:
            b30 = abs(snake.x - part[0]) + abs(snake.y - part[1])
            break
    else:
        b30 = 0

    for part in snake.body:
        if snake.x > part[0] and snake.y == part[1]:
            b0 = abs(snake.x - part[0]) + abs(snake.y - part[1])
            break
    else:
        b0 = 0

    for part in snake.body:
        if snake.x > part[0] and snake.y > part[1]:
            b02 = abs(snake.x - part[0]) + abs(snake.y - part[1])
            break
    else:
        b02 = 0

    return np.array([w0, w1, w2, w3,
                    a0, a02, a1, a31, a2, a21, a3, a30,
                    b0, b02, b1, b31, b2, b21, b3, b30,
                    ], dtype=np.float32)


class Game:
    def __init__(self):        
        self.display = pygame.display.set_mode((config.game_width, config.game_height))
        self.display.fill((220, 220, 220))
        pygame.display.set_caption('snake')
        self.color = ((220, 220, 220))
        pygame.font.init()
        self.font = pygame.font.SysFont("calibri", 18)

    def play(self):
        global snake, apple

        snake = Snake()
        apple = Apple()
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # Detect collision with apple
            if snake.x == apple.x and snake.y == apple.y:
                snake.eat()
                apple = Apple()

            snake.x_change_old, snake.y_change_old = snake.x, snake.y

            data = get_data()
            data = np.array(data)
            data = data.reshape(1, -1)
            result = model(data)
            snake.direction = np.argmax(result)

            snake.move()
     
            self.display.fill(self.color)
            pygame.draw.rect(self.display, (0, 0, 0), ((0, 0), (config.game_width, config.game_height)), 10)

            apple.draw(self.display)
            snake.draw(self.display)

            if snake.x < 0 or snake.y < 0 or snake.x > config.game_width or snake.y > config.game_height:
                self.play()

            score = self.font.render(f'Score: {snake.score}', True, ((0,0,0)))
            score_rect = score.get_rect(center=(50, 400 - 20))
            self.display.blit(score, score_rect)

            pygame.display.update()
            clock.tick(30)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--model", default="./Train/model.h5", type=str)
    args = parser.parse_args()

    model = tf.keras.models.load_model(args.model)
    game = Game()
    game.play()
