import pygame
import random


HEIGHT = 500
WIDTH = 500
SQUARE = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

SNAKE_COLORS = [WHITE, YELLOW, BLUE]

FPS = 14

def draw_grid(screen):
    for x in range(0, WIDTH, SQUARE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, SQUARE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))


pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)



def valid_food_position(food, snake):
    if food.position in snake.position:
        return False
    return True

def create_food(food):
    while food == -1:
        x, y = random.randrange(0, WIDTH // SQUARE) * 10, random.randrange(0, HEIGHT // SQUARE) * 10
        food = Food(screen, x, y)
        if not valid_food_position(food, snake):
            food = -1

    return food



class Snake():

    def __init__(self, screen):
        self.position = [[250, 250], [260, 250]]
        self.direction = [1, 0]
        self.dir_key = 1
        self.food_dist = 10000
        self.width = SQUARE
        self.screen = screen
        self.dead = False


    def update_pos(self):
        new_x = self.position[0][0] + (self.direction[0] * self.width)
        new_y = self.position[0][1] + (self.direction[1] * self.width)
        #new_x, new_y = self.correct_position(new_x, new_y)

        new_pos = [new_x, new_y]
        self.position.insert(0, new_pos)
        self.position.pop()
        # for i in range(1, len(self.position)):
        #     self.position[i], prev_pos = prev_pos, self.position[i]

        if [new_x, new_y] in snake.position[1:] or self.border_collide(new_x, new_y):
            self.draw()
            self.dead = True

    def get_keys(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.direction != [1, 0]:
            self.change_dir(0)

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.direction != [-1, 0]:
            self.change_dir(1)

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.direction != [0, 1]:
            self.change_dir(2)

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.direction != [0, -1]:
            self.change_dir(3)

    def change_dir(self, val):
        if val == 0 and self.direction != [1, 0]:
            self.direction = [-1, 0]
        elif val == 1 and self.direction != [-1, 0]:
            self.direction = [1, 0]
        elif val == 2 and self.direction != [0, 1]:
            self.direction = [0, -1]
        elif val == 3 and self.direction != [0, -1]:
            self.direction = [0, 1]

        self.dir_key = val



    def correct_position(self, x, y):
        if x >= WIDTH:
           x = 0
        elif x < 0:
            x = WIDTH

        if y >= HEIGHT:
            y = 0
        elif y < 0:
            y = HEIGHT

        return x, y

    def border_collide(self, x, y):
        if x >= WIDTH or x < 0 or  y >= HEIGHT or  y < 0:
            return True
        return False


    def draw(self):
        #snake.update_pos()
        for i in range(len(self.position)):
            rect = pygame.Rect((self.position[i][0]+1, self.position[i][1]+1), (self.width-1, self.width-1))
            pygame.draw.rect(screen, YELLOW, rect)

    def check_food(self, food):
        eaten = False

        x = self.position[0][0] + (self.direction[0] * self.width)
        y = self.position[0][1] + (self.direction[1] * self.width)
        if [x, y] == food.position or food.position == self.position[0]:
            snake.position.insert(0, [x, y])
            food = -1
            food = create_food(food)
            eaten = True

        return food, eaten

class Food():

    def __init__(self, screen, x, y):
        self.width = SQUARE
        self.position = [x, y]
        self.rect = pygame.Rect((self.position[0], self.position[1]), (self.width, self.width))
        self.screen = screen

    def draw(self):
        pygame.draw.circle(self.screen, RED, (self.position[0]+5, self.position[1]+5), 5)




pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

running = True
snake = Snake(screen)
score = 0
food = -1
food = create_food(food)


while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


    snake.get_keys()
    snake.draw()
    food.draw()
    snake.update_pos()
    food, eaten = snake.check_food(food)

    if eaten:
        score += 1


    if snake.dead:
        running = False

    text = STAT_FONT.render("Score: " + str(score), 1, (WHITE))
    screen.blit(text, (WIDTH - 10 - text.get_width(), 10))


    pygame.display.flip()
            


