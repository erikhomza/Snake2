import pygame as pg
import random


pg.init()

clock = pg.time.Clock()
fps = 30
control = 3
cooldown = 5
score = 0
highscore = 0


screen_width = 1200
screen_height = 800

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Snake")

tile_size = 50
snake = [[7,4]]
map = []
map_row = []
for i in range(24):
    map_row.append(1)
for i in range(16):
    map.append(map_row[:])
map[snake[0][0]][snake[0][1]] = 2



yellow = (255, 255, 0)
score_font = pg.font.Font("Turok.ttf", 30)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



class World():
    def __init__(self, data):
        self.tile_list = []

        ground = pg.image.load('grassCenter.png').convert_alpha()
        snake = pg.image.load('liquidLava.png').convert_alpha()
        food = pg.image.load('cakeCenter.png').convert_alpha()
        obstacle = pg.image.load('castleCenter.png').convert_alpha()

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pg.transform.scale(ground, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pg.transform.scale(snake, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pg.transform.scale(food, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pg.transform.scale(obstacle, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


def pause():
    game_paused = True
    while game_paused:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    game_paused = False
                if event.type == pg.QUIT:
                    pg.quit()


def obstacles(map):

    for i in map:
        n = random.randint(0, 23)
        map[map.index(i)][n] = 4
    return map

map = obstacles(map)

run = True
while run:

    clock.tick(fps)

    if score > highscore:
        highscore = score

    food_in_map = False
    for i in map:
        for e in i:
            if e == 3:
                food_in_map = True

    if food_in_map == False:
        y = random.randint(0, 15)
        for i in map:
            if map.index(i) == y:
                x = random.randint(0, 23)
                if i[x] == 1:
                    map[map.index(i)][x] = 3


    world = World(map)

    world.draw()
    draw_text("score " + str(score), score_font, yellow, 20, 20)
    draw_text("highscore " + str(highscore), score_font, yellow, 20, 50)



    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                pause()



    key = pg.key.get_pressed()
    if key[pg.K_DOWN]:
        if control != 2:
            control = 1
    if key[pg.K_UP]:
        if control != 1:
            control = 2
    if key[pg.K_RIGHT]:
        if control != 4:
            control = 3
    if key[pg.K_LEFT]:
        if control != 3:
            control = 4


    cooldown-=1
    if cooldown == 0:


        if control == 3:
            temp = snake[-1]
            snake.append(temp[:])
            snake[-1][1] += 1

        if control == 4:
            temp = snake[-1]
            snake.append(temp[:])
            snake[-1][1] -= 1

        if control == 1:
            temp = snake[-1]
            snake.append(temp[:])
            snake[-1][0] += 1

        if control == 2:
            temp = snake[-1]
            snake.append(temp[:])
            snake[-1][0] -= 1

        if snake[-1][0] == 16:
            snake[-1][0] -= 16
        if snake[-1][1] == 24:
            snake[-1][1] -= 24
        if snake[-1][0] == -1:
            snake[-1][0] = 15
        if snake[-1][1] == -1:
            snake[-1][1] = 23


        eating = False
        if map[snake[-1][0]][snake[-1][1]] == 2 or map[snake[-1][0]][snake[-1][1]] == 4:
            map = []
            map_row = []
            for i in range(24):
                map_row.append(1)
            for i in range(16):
                map.append(map_row[:])
            map = obstacles(map)
            snake = [[7, 4], [7, 5]]
            score = 0
            map[snake[0][0]][snake[0][1]] = 2
            map[snake[1][0]][snake[1][1]] = 2
        if map[snake[-1][0]][snake[-1][1]] == 3:
            eating = True
            score += 1
        map[snake[-1][0]][snake[-1][1]] = 2
        if eating == False:
            map[snake[0][0]][snake[0][1]] = 1
            snake.pop(0)
        cooldown = 5



    pg.display.update()

pg.quit()