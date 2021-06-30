import pygame
from pygame.locals import * 

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 675
screen_height = 732

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#game variables.
ground_scroll = 0
scroll_speed = 4 
flying = False
game_over = False

#loading images.
bg = pygame.image.load('images/bg1.png')
ground_img = pygame.image.load('images/ground1.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.count = 0
        for num in range(1, 4):
            img = pygame.image.load(f'images/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 6.25:
                self.vel = 6.25
            if self.rect.bottom < 600:
                self.rect.y += int(self.vel)

        if game_over == False:
            #jumping
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.vel = -10
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #animation
            self.count += 1
            flap_cooldown = 5

            if self.count > flap_cooldown:
                self.count = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotating the images(bird)
            self.image = pygame.transform.rotate(self.images[self.index], (-2) * self.vel)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)


run = True
while run:

    clock.tick(fps)

    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()

    #draw the ground
    screen.blit(ground_img, (ground_scroll, 600))

    #checking for ending of game
    if flappy.rect.bottom > 600:
        game_over = True
        flying = False


    if game_over == False:
        #moving the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()