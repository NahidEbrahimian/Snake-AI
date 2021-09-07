from argparse import ArgumentParser
import random
from tqdm import tqdm
from snake import Snake
from apple import Apple
import config


def add_data():
    # distance-wall
    w0 = snake.x - config.wall_offset  # left
    w1 = config.game_width - config.wall_offset - snake.x  # right
    w2 = snake.y - config.wall_offset  # up
    w3 = config.game_height - config.wall_offset - snake.y  # down

    # distance-apple
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

    # distance-body
    for part in snake.body:
        if snake.x > part[0] and snake.y == part[1]:
            b0 = abs(snake.x - part[0]) + abs(snake.y - part[1])
            break
    else:
        b0 = 0

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
        if snake.x > part[0] and snake.y > part[1]:
            b02 = abs(snake.x - part[0]) + abs(snake.y - part[1])
            break
    else:
        b02 = 0

    direction = snake.direction
    if snake.direction != snake.pre_direction or random.random() < 0.05:
        f.write(','.join([str(w0), str(w1), str(w2), str(w3),
                          str(a0), str(a02), str(a1), str(a31), str(a2), str(a21), str(a3), str(a30),
                          str(b0), str(b02), str(b1), str(b31), str(b2), str(b21), str(b3), str(b30),
                          str(direction)]) + '\n')
        return True

    else:
        return False


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--num_generate_rows", type=int)
    parser.add_argument("--dataset", default="./Dataset.csv", type=str)
    args = parser.parse_args()

    f = open(args.dataset, 'w')
    f.write('w0,w1,w2,w3,a0,a02,a1,a31,a2,a21,a3,a30,b0,b02,b1,b31,b2,b21,b3,b30,direction' + '\n')

    rows = 0
    pbar = tqdm(total=100, position=0, leave=True)

    snake = Snake()
    apple = Apple()

    while rows < args.num_generate_rows:
        # Detect collision with apple
        if snake.x == apple.x and snake.y == apple.y:
            snake.Eat()
            apple = Apple()

        # collision with body
        for part in snake.body:
            if snake.x == part[0] and snake.y == part[1]:
                snake = Snake()

        direction = snake.vision(apple)
        snake.pre_direction = snake.direction
        snake.decision(direction)

        if snake.collision_with_wall(snake.direction):
            direction = (snake.direction + 1) % 4
            if snake.collision_with_wall(direction):
                direction = (snake.direction - 1) % 4
                if snake.collision_with_wall(direction):
                    snake = Snake()

            snake.direction = direction

        if add_data():
            rows += 1
            pbar.update(0.0001)

        snake.move()

    f.close()
