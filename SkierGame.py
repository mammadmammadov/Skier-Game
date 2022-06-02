import cfg
import pygame
import random
import sys

# pygame.sprite.Sprite -  Simple base class for visible game objects.


class SkierClass(pygame.sprite.Sprite):  # SkierClass inherits from pygame.sprite.Sprite;

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.direction = 0
        self.imagepaths = cfg.SKIER_IMAGE_PATHS[:-1]  # all pictures except the last one
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.speed = [self.direction, self.direction]  # related to position change
        
    def turn(self, num):
        self.direction += num
        
        self.direction = max(-2, self.direction)  # here -2 means turning left two times, since we can turn left max 2 time
        # it is written in this way
        
        self.direction = min(2, self.direction)  # same scenario with turning right, but it will be in min because of right     
        
        center = self.rect.center
        self.image = pygame.image.load(self.imagepaths[self.direction])  # getting image for the relevant position
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = [self.direction, 4 - abs(self.direction)]
        return self.speed
    
    def move(self):
        self.rect.centerx += self.speed[0]
        
        # making sure that the skier stays within the window
        self.rect.centerx = max(30, self.rect.centerx)
        self.rect.centerx = min(600, self.rect.centerx)
    
    def setFall(self):
        self.image = pygame.image.load(cfg.SKIER_IMAGE_PATHS[-1])  # getting the last image
     
    def setForward(self):
        self.direction = 0;  # gets back to straight position each time the skier fails
        self.image = pygame.image.load(self.imagepaths[self.direction])


class ObstacleClass(pygame.sprite.Sprite):

    def __init__(self, imagePath, location, attribute):
        pygame.sprite.Sprite.__init__(self)            
        self.imagePath = imagePath
        self.image = pygame.image.load(self.imagePath)
        self.location = location
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.attribute = attribute
        self.passed = False  # default
        
    def move(self, num):
        self.rect.centery = self.location[1] - num + 1  # +1 is optional

    
def CreateObstacle(s, e, num=30):
    obstacles = pygame.sprite.Group()  # group of items that will be displayed
    locations = []  # empty list
    
    for j in range (num):
        row = random.randint(s, e)  # random number between s and e
        column = random.randint(0, 8)
        location = [column * 64 + 30 , row * 64 + 30]
        if location not in locations:
            locations.append(location)
            attribute = random.choice(list(cfg.OBSTACLE_PATHS.keys()))  # returns a randomly selected element from the list
            imagePath = cfg.OBSTACLE_PATHS[attribute]
            obstacle = ObstacleClass(imagePath, location, attribute)
            obstacles.add(obstacle)
    return obstacles    


def AddObstacles(obstacle_0, obstacle_1):
    obstacles = pygame.sprite.Group()
    for obstacle in obstacle_0:
        obstacles.add(obstacle)
    for obstacle in obstacle_1:
        obstacles.add(obstacle)
    return obstacles       


def ShowStartInterface(screen, screensize):
    screen.fill((212, 255, 255))
    titleFont = pygame.font.Font(cfg.FONT_PATH, screensize[0] // 6)
    contentFont = pygame.font.Font(cfg.FONT_PATH, screensize[0] // 22)
    title = titleFont.render('Skier Game', True, (255, 0, 0))  # True shows that the title is smooth
    content = contentFont.render('Press Any Key to Start. (Except Power Key xD)', True, (255, 0, 0))
    titleRectangle = title.get_rect()
    titleRectangle.midtop = (screensize[0] / 2.05, screensize[1] / 5.05)
    contentRectangle = content.get_rect()
    contentRectangle.midtop = (screensize[0] / 2.05, screensize[1] / 2.05)
    screen.blit(title, titleRectangle)  # blit draws on surface
    screen.blit(content, contentRectangle)
    
    # code below allows the user to quit the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.update()  # displays on screen


def ShowEndInterface(screen, screensize):
    screen.fill((212, 255, 255))
    titleFont = pygame.font.Font(cfg.FONT_PATH, screensize[0] // 5)
    title = titleFont.render('You Lost!', True, (255, 0, 0))
    titleRectangle = title.get_rect()
    titleRectangle.midtop = (screensize[0] / 2.05, screensize[1] / 5)
    screen.blit(title, titleRectangle) 
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()

        
def showScore(screen, score, pos=(10, 10)):
    font = pygame.font.Font(cfg.FONT_PATH, 30)
    scoreText = font.render("Score: %s" % score, True, (0, 0, 0))
    screen.blit(scoreText, pos)

    
def updateFrame(screen, obstacles, skier, score):
    screen.fill((243, 253, 255))
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    showScore(screen, score)
    pygame.display.update()

    
def main():
    pygame.init()
    pygame.mixer.init()  # we initialize this for being able to play the music
    pygame.mixer.music.load(cfg.MUSIC_PATH)
    pygame.mixer.music.set_volume(0.2)  # 0.2 of the computer's volume
    pygame.mixer.music.play(-1)  # for playing song infinitely
    
    screen = pygame.display.set_mode(cfg.WINDOWS_SIZE)
    pygame.display.set_caption('Skier Game')
    
    ShowStartInterface(screen, cfg.WINDOWS_SIZE)
    
    skier = SkierClass()
    
    obstacles0 = CreateObstacle(20, 29)
    obstacles1 = CreateObstacle(10, 19)
    obstaclesFlag = 0
    obstacles = AddObstacles(obstacles0, obstacles1)
    distance = 0
    score = 0
    speed = [0, 6]
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    speed = skier.turn(-1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    speed = skier.turn(1)    
        skier.move()
        distance += speed[1]
        if distance >= 640 and obstaclesFlag == 0:
            obstaclesFlag = 1
            obstacles0 = CreateObstacle(20, 29)
            obstacles = AddObstacles(obstacles0, obstacles1)
            
        if distance >= 1280 and obstaclesFlag == 1:
            obstaclesFlag = 0
            distance -= 1280
            for obstacle in obstacles0:
                obstacle.location[1] = obstacle.location[1] - 1280
            obstacles1 = CreateObstacle(10, 19)
            obstacles = AddObstacles(obstacles0, obstacles1)               
        
        for obstacle in obstacles:
            obstacle.move(distance)
            
        hittedObstacles = pygame.sprite.spritecollide(skier, obstacles, False)
        
        if hittedObstacles:
            if hittedObstacles[0].attribute == "tree" and not hittedObstacles[0].passed:
                score -= 30
                skier.setFall()
                updateFrame(screen, obstacles, skier, score)
                pygame.time.delay(500)
                skier.setForward()
                speed = [0, 6]
                hittedObstacles[0].passed = True
            elif hittedObstacles[0].attribute == "flag" and not hittedObstacles[0].passed:
                score += 10
                obstacles.remove(hittedObstacles[0])  # for making the flag disappear from the screen
            if score <= 0:
                pygame.mixer.music.stop()
                ShowEndInterface(screen, cfg.WINDOWS_SIZE)
                
        updateFrame(screen, obstacles, skier, score) 
        clock.tick(cfg.FPS)     
        
            
if __name__ == '__main__':
    main()    

