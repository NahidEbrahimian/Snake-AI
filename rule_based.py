import pygame
from snake import Snake
from apple import Apple
import config


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((config.game_width, config.game_height))
        self.color = ((220, 220, 220))
        self.display.fill((220, 220, 220))
        pygame.display.set_caption('Snake-AI')
        pygame.font.init()
        self.font = pygame.font.SysFont("calibri", 18)

    def play(self):
        snake = Snake()
        apple = Apple()
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # Apple position
            if snake.x == apple.x and snake.y == apple.y:
                snake.Eat()
                apple = Apple()

            # Snake: Collision with body
            for part in snake.body:
                if snake.x == part[0] and snake.y == part[1]:
                    snake = Snake()

            direction = snake.vision(apple)
            snake.pre_direction = snake.direction
            snake.decision(direction)

            # Snake: Collision with wall
            if snake.collision_with_wall(snake.direction):
                if snake.direction == 0:
                    direction = 2

                elif snake.direction == 2:
                    direction = 1

                elif snake.direction == 3:
                    direction = 0

                elif snake.direction == 1:
                    direction = 3

                if snake.collision_with_wall(direction):

                    if snake.direction == 0:
                        direction = 3

                    elif snake.direction == 2:
                        direction = 30

                    elif snake.direction == 3:
                        direction = 1

                    elif snake.direction == 1:
                        direction = 2

                    if snake.collision_with_wall(direction):
                        snake = Snake()

                snake.direction = direction

            snake.move()

            self.display.fill(self.color)
            pygame.draw.rect(self.display, ((80, 80, 80)), ((0, 0), (600,400)), 10)

            apple.draw(self.display)
            snake.draw(self.display)

            score = self.font.render(f'Score: {snake.score}', True, ((0,0,0)))
            score_rect = score.get_rect(center=(50, 400 - 20))
            self.display.blit(score, score_rect)

            pygame.display.update()
            clock.tick(10)


if __name__ == "__main__":

    game = Game()
    game.play()
